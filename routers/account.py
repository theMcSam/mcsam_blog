from fastapi import APIRouter, Request, Depends, HTTPException
from blog.database import db_session
from blog.errors import DeletedSuccessfully, IncorrectUsernameOrPassword
from blog.models import User
from schemas.account import Account
from utils.utils import account_owner, get_user_id_from_token

from jwt import InvalidTokenError
import jwt
import os
import bcrypt

account = APIRouter(prefix="/api/account",tags=["Account Operations"])


def verify_token(req: Request):
    token = req.headers["Authorization"] if "Authorization" in req.headers else False

    if token is False:
        return False

    try:
        jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms="HS256")
        return True

    except InvalidTokenError:
        return False


# @account.put("/api/account/update/{user_id}")
# def update_account(user_id, account: Account):
#     user = db_session.query(User).get(user_id)
#     if user:
#         ...
#     raise HTTPException(404, "User does not exist.")

@account.delete("/delete/{account_id}")
def delete_account(account_id, accounts: Account, req: Request, authorized: bool = Depends(verify_token)):
    if not authorized:
        raise HTTPException(403, "You are not authorized.")

    user_id = get_user_id_from_token(req.headers["Authorization"])
    if not account_owner(user_id, account_id):
        raise HTTPException(403, "You do not own this account.")

    user = db_session.query(User).filter(User.user_id == user_id).first()
    if user:
        if bcrypt.checkpw(accounts.password.encode(), str(user.password).encode()):
            db_session.delete(user)
            db_session.commit()

            raise DeletedSuccessfully

        raise IncorrectUsernameOrPassword

    raise IncorrectUsernameOrPassword
