from pydantic import BaseModel

class user_resister(BaseModel):
    username : str
    email : str
    password : str
    model_config={"from_attributes":True}

class user_login(BaseModel):
    identifier: str
    password : str

class user_text(BaseModel):
    text: str

class user_title(BaseModel):
    title_id : int

class new_title(BaseModel):
    title_text : str

class TokenData(BaseModel):
    id: int | None = None  