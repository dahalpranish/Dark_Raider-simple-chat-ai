from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schemas,model,authentication
from database import get_db
from passlib.context import CryptContext


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def hash(password):
    return pwd_cxt.hash(password)

def verify(hashed_password,plain_password):
    return pwd_cxt.verify(plain_password,hashed_password )


router = APIRouter(prefix="/user")



@router.post("/resister",tags=[ "Register"])
def resister(request:schemas.user_resister,db: Session = Depends(get_db)):
    existing_email = db.query(model.user_resister).filter(model.user_resister.email == request.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    existing_username = db.query(model.user_resister).filter(model.user_resister.username == request.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="username already exists")
    user = model.user_resister(username = request.username, email = request.email, password = hash(request.password))
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Registration successful"}

@router.post("/login", tags=["login_authentication"])
def login(request: schemas.user_login, db: Session = Depends(get_db)):
    user = db.query(model.user_resister).filter(
        (model.user_resister.username == request.identifier) |
        (model.user_resister.email == request.identifier)
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    if not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = authentication.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}