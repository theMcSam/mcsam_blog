from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserSignUp(UserLogin):
    email: str