from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user import UserCreate,UserLog,refresh_token
from app.core.auth import SECRET_KEY, ALGORITHM, create_refresh_token
from app.core.db import get_db
from app.core.auth import create_token,hash_password,verify_password
from jose import jwt,JWTError
from app.core.logging import logger
router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()

    if existing:
        logger.warning(f"Failed registering attempt for username {user.username}")
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"New user registered: {new_user.username}")
    
    return {"message": "User created"}

@router.post("/login")
def login(user: UserLog, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        logger.warning(f"Failed login attempt for username {user.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub":str (db_user.id)})
    refresh_token = create_refresh_token({"sub":str (db_user.id)})

    logger.info(f"User {db_user.username} logged in")
    

    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(data:refresh_token):

    try:
        payload = jwt.decode(
            data.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            logger.error("Refresh failed: missing user_id in token")
            raise HTTPException(status_code=401, detail="Invalid token")

        new_access_token = create_token(
            {"sub": user_id}
        )
        
        logger.info(f"User {user_id} requested token refresh")
        return {"access_token": new_access_token}
    
    except JWTError:
        logger.error("Invalid refresh token used")
        raise HTTPException(status_code=401, detail="Invalid refresh token")
