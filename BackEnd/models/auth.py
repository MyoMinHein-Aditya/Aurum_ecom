from pydantic import BaseModel, EmailStr, Field

class UserRegisterReq(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="Password")

class UserLoginReq(BaseModel):
    email: EmailStr
    password: str

class UserResp(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True

class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"
