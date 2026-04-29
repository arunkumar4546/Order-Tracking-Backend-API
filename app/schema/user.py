from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLog(BaseModel):
    username:str
    password:str

class UserResp(BaseModel):
    id:int
    username:str
    
    class Config:
        from_attributes = True
        
class refresh_token(BaseModel):
    refresh_token:str