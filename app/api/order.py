from fastapi import APIRouter,Depends,HTTPException
from app.schema.order import OrderCreate,OrderStatusUpdate,OrderResponse
from app.models.order import Order,Orderhistory
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.constants import VALID_STATUS_FLOW
from app.core.auth import get_current_user,get_admin_user
from app.core.logging import logger


router = APIRouter()

@router.post("/place")
def create_orders(order:OrderCreate,
                  db:Session=Depends(get_db),
                  current_user=Depends(get_current_user)):
    new_order=Order(item_name=order.item_name,quantity=order.quantity,user_id=current_user.id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    logger.info(f"User {current_user.id} placed order {new_order.id}")

    return {
        "message":"Order placed",
        "order_id":new_order.id
    }

@router.get("/view", response_model=list[OrderResponse])
def get_orders(skip: int = 0,
               limit: int = 10,
               db:Session=Depends(get_db),
               current_user=Depends(get_current_user)):
     logger.info(f"User {current_user.id} viewed orders")
     return db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()

@router.get("/view/{order_id}")
def get_order(order_id: int, 
              db: Session = Depends(get_db),
              current_user=Depends(get_current_user)):
    
    order = db.query(Order).filter(Order.id == order_id,Order.user_id==current_user.id).first()

    if not order:
        logger.warning(f"Unauthorized access: user {current_user.id} tried order {order_id}")
        raise HTTPException(status_code=404, detail="Order not found")      
    logger.info(f"User {current_user.id} accessed order {order_id}")
    
    return order

@router.get("/allorders", response_model=list[OrderResponse])
def get_all_orders(db: Session = Depends(get_db),current_user = Depends(get_admin_user)):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return orders

@router.patch("/{order_id}/status")
def update_order_status(order_id: int, status: OrderStatusUpdate, db: Session = Depends(get_db),
                        current_user=Depends(get_admin_user)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        logger.warning(f"Admin {current_user.id} attempted to update non-existent order {order_id}")
        raise HTTPException(status_code=404, detail="Order not found")

    current_status = order.status
    new_status = status.status.value
    if new_status not in VALID_STATUS_FLOW[current_status]:
        logger.error(f"Invalid status update attempt on order {order_id}: {current_status} → {new_status}")
        raise HTTPException(status_code=400,detail="Invalid status flow")
    order.status = status.status.value
    history=Orderhistory(order_id=order.id,
                         item_name=order.item_name, 
                         quantity=order.quantity, 
                         status=order.status
                        )
    db.add(history)
    db.commit()
    db.refresh(order)
    logger.info(f"Admin {current_user.id} updated order {order.id} status to {order.status}")
    return order

@router.get("/{order_id}/track")
def track_order_history(order_id: int, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    
    order = db.query(Order).filter(Order.id == order_id,Order.user_id == current_user.id).first()
    
    if not order:
        logger.warning(f"Unauthorized access to history: user {current_user.id}, order {order_id}")
        raise HTTPException(status_code=403, detail="Not allowed")
    logger.info(f"User {current_user.id} viewed history for order {order_id}")
    return order.history