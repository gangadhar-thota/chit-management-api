from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.bids import Bid as BidModel
from app.models.chit_member import ChitMember
from app.models.installment import Installment as InstallmentModel
from app.schemas.bids import BidCreate, BidUpdate
from fastapi import HTTPException, status


def get_all(db: Session, chit_id: int = None):
    query = db.query(BidModel)
    if chit_id:
        query = query.filter(BidModel.chit_id == chit_id)
    return query.all()


def get_by_id(db: Session, bid_id: int):
    return db.query(BidModel).filter(BidModel.id == bid_id).first()


def get_last_bid(db: Session, installment_id: int):
    return (
        db.query(BidModel)
        .filter(BidModel.installment_id == installment_id)
        .order_by(desc(BidModel.created_at))
        .first()
    )


def create(db: Session, payload: BidCreate, user_id: int):
    # Check installment exists
    installment = db.query(InstallmentModel).filter(InstallmentModel.id == payload.installment_id).first()
    if not installment:
        raise HTTPException(status_code=404, detail="Installment not found")

    # Check if winner already declared
    if installment.winner_id:
        raise HTTPException(status_code=400, detail="Winner already declared")
        
    # Check if the member already took the chit
    member = db.query(ChitMember).filter(
        ChitMember.member_id == payload.member_id,
        ChitMember.chit_id == payload.chit_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found in this chit")

    if member.is_taken:
        raise HTTPException(status_code=400, detail="Member already took the chit. Cannot bid.")

    # Get last bid for the installment
    last_bid = get_last_bid(db, payload.installment_id)

    if last_bid:
        if last_bid.member_id == payload.member_id:
            raise HTTPException(status_code=400, detail="You cannot place consecutive bids.")
        if payload.bid_amount <= float(last_bid.bid_amount):
            raise HTTPException(status_code=400, detail="Bid amount must be higher than previous bid.")

    db_bid = BidModel(
        chit_id=payload.chit_id,
        installment_id=payload.installment_id,
        member_id=payload.member_id,
        bid_amount=payload.bid_amount,
        created_by=user_id
    )
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid


def update(db: Session, bid_id: int, payload: BidUpdate):
    bid = get_by_id(db, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")

    if payload.bid_amount is not None:
        bid.bid_amount = payload.bid_amount

    db.commit()
    db.refresh(bid)
    return bid

def get_highest_bid(installment_id: int, db: Session):
    return (
        db.query(BidModel)
        .filter(BidModel.installment_id == installment_id)
        .order_by(BidModel.bid_amount.desc())
        .first()
    )    


def declare_winner(installment_id: int, db: Session):   
    # 2. Check installment exists
    installment = db.query(InstallmentModel).filter(InstallmentModel.id == installment_id).first()
    if not installment:
        raise HTTPException(status_code=404, detail="Installment not found")

    # 3. Check if winner already declared
    if installment.winner_id:
        raise HTTPException(status_code=400, detail="Winner already declared")

    # 4. Get highest bid using repo
    highest_bid = get_highest_bid(installment_id, db)
    if not highest_bid:
        raise HTTPException(status_code=400, detail="No bids placed")

    # 5. Update installment
    installment.bid_amount = highest_bid.bid_amount
    installment.winner_id = highest_bid.member_id

    # 6. Update chit_member
    chit_member = (
        db.query(ChitMember)
        .filter(
            ChitMember.chit_id == installment.chit_id,
            ChitMember.member_id == highest_bid.member_id,
        )
        .first()
    )

    if not chit_member:
        raise HTTPException(status_code=404, detail="Chit member not found")

    chit_member.is_taken = True
    chit_member.bid_amount = highest_bid.bid_amount
    chit_member.taken_installment = installment.installment_no

    db.commit()

    return {
        "message": "Winner declared successfully",
        "winner_id": highest_bid.member_id,
        "bid_amount": highest_bid.bid_amount,
    }    
