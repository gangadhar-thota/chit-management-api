from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chit_api, user_api, member_api, chit_member_api, installment_api,bid_api

app = FastAPI(title="Chit Management App")

# Allow requests from your frontend
origins = [
    "http://localhost:3000",  # React or other frontend running on this port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # restrict to only your frontend in dev
    allow_credentials=True,
    allow_methods=["*"],           # allow all HTTP methods
    allow_headers=["*"],           # allow all headers
)

app.include_router(chit_api.router)
app.include_router(member_api.router)
app.include_router(chit_member_api.router)
app.include_router(installment_api.router)
app.include_router(bid_api.router)
app.include_router(user_api.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Welcome to Chit Management App By Gangadhar"}
