"""
auth.py
Authentication routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from BackEnd.database.connection import get_db
from BackEnd.database.models import User
from BackEnd.models.auth import UserRegisterReq, UserLoginReq, UserResp, TokenResp
from BackEnd.services import auth_service
from BackEnd.utils.security import verify_password, create_access_token, create_refresh_token
from BackEnd.utils.deps import get_current_user

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserResp)
def register(request: Request, user_data: UserRegisterReq, db: Session = Depends(get_db)):
    """Registers a new user."""
    return auth_service.register_user(db, user_data)

@router.post("/login", response_model=TokenResp)
def login(request: Request, user_data: UserLoginReq, response: Response, db: Session = Depends(get_db)):
    """Authenticates a user and returns a JWT."""
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="lax",
        secure=False, # Set True in prod
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(request: Request, response: Response):
    """Logs out a user by clearing the refresh token."""
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResp)
def read_users_me(request: Request, current_user: User = Depends(get_current_user)):
    """Returns the current user."""
    return current_user
