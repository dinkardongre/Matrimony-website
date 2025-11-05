from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.utils.dtos import UserSchema, ProfileSchema,  LoginSchema, UpdatePasswordSchema, ForgetPasswordSchema, VerifyOtpSchema
from src.db.db import get_db
from src.controllers.user_controller import *
from src.dependencies.auth import is_authenticated

userRouter = APIRouter(prefix="/users")

@userRouter.post("/register")
def register_user(body:UserSchema, db:Session = Depends(get_db)):
    return register(body, db)

@userRouter.post("/login")
def login_user(body:LoginSchema, db:Session = Depends(get_db)):
    return login(body, db)

@userRouter.post("/updatePassword")
def update_password(body:UpdatePasswordSchema, db:Session = Depends(get_db), user: User = Depends(is_authenticated)):
    return updatePassword(body, db, user)

@userRouter.post("/forgetPassword")
def forget_password(body:ForgetPasswordSchema, db:Session = Depends(get_db)):
    return forgetPassword(body, db)

@userRouter.post("/verifyOtp")
def verify_otp(body:VerifyOtpSchema, db:Session = Depends(get_db)):
    return verifyOtp(body, db)

@userRouter.put("/")
def update_user(body:UserSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return updateUser(body, db, user)

@userRouter.delete("/")
def delete_user(db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return deleteUser(db, user)

@userRouter.get("/profile")
def get_user_profile(db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return getUserProfile(db, user)

@userRouter.post("/profile")
def create_user_profile(body:ProfileSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return createUserProfile(body, db, user)

@userRouter.put("/profile")
def update_user_profile(body:ProfileSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return updateUserProfile(body, db, user)