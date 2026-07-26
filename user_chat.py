from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
import schemas,model,oauth2
from database import get_db
from google import genai
from dotenv import load_dotenv

load_dotenv()


router= APIRouter(prefix="/user")
ai_client = genai.Client()
@router.get("/titles",tags=["title"])
def all_title_show(db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user_id = current_user.id
    titles = db.query(model.user_title).filter(model.user_title.user_id == user_id).all()
    all_title = [{"title_id":title.title_id,"title":title.title_text} for title in titles]
    all_title.sort(key=lambda x: x["title_id"], reverse=True)
    return {"title" : all_title}

@router.post("/title/chat",tags=["title"])
def create_title(request : schemas.new_title, db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user_id = current_user.id
    title = model.user_title(title_text = request.title_text, user_id= user_id)
    db.add(title)
    db.commit()
    db.refresh(title)
    return({"title": title.title_text,"title_id": title.title_id})



@router.get("/title/chat/{titleid}",tags=["chat"])
def chat_history(titleid:int,db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user_id = current_user.id
    chats = db.query(model.user_chat).filter(model.user_chat.user_id == user_id, model.user_chat.title_id == titleid).all()
    history = [{"user_text": chat.user_text,"server_text": chat.server_text} for chat in chats]
    return { "history": history}

@router.post("/title/chat/{titleid}",tags=["chat"])
def user_chat(titleid:int,request: schemas.user_text,db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    try:
        # 1. Send the incoming request text to Gemini
        # Using 'gemini-2.5-flash', which is fast, cheap, and ideal for chat applications
        response = ai_client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=request.text
        )
        
        # 2. Extract the generated text response
        ai_reply = response.text
        
    except Exception as e:
        # Catch network issues or API limits gracefully
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemini API Error: {str(e)}"
        )
    
    user_id = current_user.id
    text = model.user_chat(user_id=user_id, user_text=request.text, server_text=ai_reply, title_id=titleid)
    if not text:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="something went wrong!!")
    db.add(text)
    db.commit()
    db.refresh(text)
    return {"reply":text.server_text}

