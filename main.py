from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db,engine
import model,userandhashing,user_chat  


app = FastAPI()
app.include_router(userandhashing.router)
app.include_router(user_chat.router)
model.Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten this to your actual frontend origin later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
