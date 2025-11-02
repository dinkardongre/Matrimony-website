from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from src.core.congif import SECRET_KEY, ALGORITHM
from src.controllers.user_controller import get_user_by_username
from src.db.db import get_db


def is_authenticated(
    req: Request,
    db: Session = Depends(get_db)
 ):
    token = req.headers.get("authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "You are not authorized"}
        )
    
    token = token.split(" ")[-1]  # remove "Bearer"
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token has expired"}
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token"}
        )
    
    username = data.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "You are not authorized"}
        )
    
    user = get_user_by_username(username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "You are not authorized"}
        )
    
    return user