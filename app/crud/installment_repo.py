from sqlalchemy.orm import Session
from app.models.installment import Installment
from app.schemas.installment import InstallmentCreate, InstallmentUpdate

def create_installment(db: Session, data: InstallmentCreate, user_id: int):
    existing = db.query(Installment).filter(
        Installment.chit_id == data.chit_id,
        Installment.installment_no == data.installment_no,
        Installment.created_by == user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Installment #{data.installment_no} for chit {data.chit_id} already exists."
        )
        
    db_item = Installment(**data.dict(), created_by=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all(db: Session, user_id: int):
    return db.query(Installment).filter(Installment.created_by == user_id).all()

def get_by_id(db: Session, installment_id: int, user_id: int):
    return db.query(Installment).filter(
        Installment.id == installment_id,
        Installment.created_by == user_id
    ).first()

def update_installment(db: Session, installment_id: int, update_data: InstallmentUpdate, user_id: int):
    db_item = get_by_id(db, installment_id, user_id)
    if not db_item:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item
