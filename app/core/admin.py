from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from app.core.logging import logger

load_dotenv()

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
ADMIN_USERNAME=os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")

def create_admin(db: Session):

    admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()

    if admin:
        logger.debug("Admin user already exists")
        return

    hashed_pw = pwd.hash(ADMIN_PASSWORD)

    new_admin = User(
        username=ADMIN_USERNAME,
        password=hashed_pw,
        role="admin"
    )

    db.add(new_admin)
    db.commit()
    logger.info("Admin user created successfully")