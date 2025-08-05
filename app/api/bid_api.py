from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.bids import Bid, BidCreate, BidUpdate
from app.crud import bid_repo
from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from app.utils.auth_router import get_authenticated_router

router = get_authenticated_router(
    prefix="/bids",
    tags=["Bids"]
)


@router.get("/", response_model=List[Bid])
def get_all_bids(chit_id: int = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return bid_repo.get_all(db, chit_id)


@router.get("/{bid_id}", response_model=Bid)
def get_bid(bid_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    bid = bid_repo.get_by_id(db, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return bid


@router.post("/", response_model=Bid)
def create_bid(payload: BidCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return bid_repo.create(db, payload, user_id=user.id)


@router.put("/{bid_id}", response_model=Bid)
def update_bid(bid_id: int, payload: BidUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return bid_repo.update(db, bid_id, payload)

@router.get("/declare-winner/{installment_id}")
def declare_winner(
    installment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):   
    return bid_repo.declare_winner(installment_id, db) 