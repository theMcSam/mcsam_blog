from fastapi import APIRouter
from blog.database import db_session

account = APIRouter()

@account.put("/api/account/update/{user_id}")
def update_account(user_id):
    ...