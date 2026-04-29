from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    quantity = Column(Integer)
    status = Column(String, default="PLACED")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer,ForeignKey("users.id"))

    user=relationship("User", back_populates="orders")
    history = relationship("Orderhistory", back_populates="order")

class Orderhistory(Base):
    __tablename__ = "orderhistory"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    item_name = Column(String)
    quantity = Column(Integer)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="history")