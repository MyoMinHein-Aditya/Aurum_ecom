"""
auth_service.py
Business logic for authentication.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from BackEnd.database.models import User
from BackEnd.models.auth import UserRegisterReq
from BackEnd.utils.security import get_password_hash

def register_user(db: Session, user_data: UserRegisterReq) -> User:
    """Registers a new user."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    # First user can be admin for demo purposes if we wanted, but let's stick to false.
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
