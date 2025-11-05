import jwt as pyjwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.utils.dtos import UserSchema, ProfileSchema, LoginSchema, UpdatePasswordSchema, ForgetPasswordSchema, VerifyOtpSchema
from src.models.user_model import User, Profile
from src.core.congif import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from src.core.security import get_password_hash, verify_password
def get_user_by_username(username: str, database: Session):
    return database.query(User).filter(User.username == username).first()

def register(body: UserSchema, database: Session):
    currentUser = get_user_by_username(body.username, database)
    if currentUser:
        raise HTTPException(409, detail={"Error": "User already exists"})

    hashed_pw = get_password_hash(body.password)

    user = User(
        name=body.name,
        gender=body.gender,
        email=body.email,
        phone=body.phone,
        username=body.username,
        hash_password=hashed_pw,
        date_of_birth=body.date_of_birth,
        is_active=body.is_active
    )

    database.add(user)
    database.commit()
    database.refresh(user)

    return {"status": "User created successfully"}

def login(body: LoginSchema, database: Session):
    currentUser = get_user_by_username(body.username, database)
    if not currentUser:
        raise HTTPException(404, detail={"Error": "User not found"})

    if not verify_password(body.password, currentUser.hash_password):
        raise HTTPException(401, detail="Password is incorrect")

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = pyjwt.encode(
        {"username": currentUser.username, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"message": "Login successful", "token": token}

def updatePassword(body:UpdatePasswordSchema,db:Session, user: User):
    currentUser = db.query(User).filter(User.id == user.id).first()
    if not currentUser:
        raise HTTPException(404, detail={"Error":"User not found"})
    
    if not verify_password(body.old_password, currentUser.hash_password):
        raise HTTPException(401, detail="Old Password is incorrect")

    if body.old_password == body.new_password:
        raise HTTPException(400, detail={"Error":"New password cannot be the same as the old one"})
    
    hashed_pw = get_password_hash(body.new_password)

    currentUser.hash_password = hashed_pw
    
    db.commit()
    db.refresh(currentUser)

    return {
        "Status":"Password updated successfully.."
    }

import random

def forgetPassword(body:ForgetPasswordSchema, db:Session):
    currentUser = db.query(User).filter(User.email == body.email).first()
    if not currentUser:
        raise HTTPException(404, detail={"Error":"User not exists"})
    newOtp = str(random.randint(1000, 9999))

    currentUser.otp = newOtp

    db.commit()
    db.refresh(currentUser)

    print("One time password -> ",newOtp)

    return {"Status":"Otp sends on the email address.."}

def verifyOtp(body:VerifyOtpSchema, db:Session):
    currentUser = db.query(User).filter(User.email == body.email).first()
    if not currentUser:
        raise HTTPException(404, detail={"Error":"User not exists"})
    if currentUser.otp != body.otp:
        raise HTTPException(404, detail={"Error":"otp is incorrect. Try again..."})
    
    hashed_pw = get_password_hash(body.new_password)
    
    currentUser.hash_password = hashed_pw
    currentUser.otp = None
    db.commit()
    db.refresh(currentUser)
    
    return {
        "Status2":"Your password is updated.."
    }

def getUserProfile(db:Session, user:User):
    user = db.query(User).filter(User.id == user.id).first()
    if not user:
        raise HTTPException(404, detail={"Error":"User not exist"})
    return {
        "Status":"Users details..",
        "User's Details":{
            "id":user.id,
            "username":user.username,
            "name":user.name,
            "gender":user.gender,
            "email":user.email,
            "phone":user.phone,
            "Account creation":user.created_at
        },
        "Profile":user.profile
    }

def updateUser(body:UserSchema, db:Session, user:User):
    currentUser = db.query(User).filter(User.id == user.id).first()
    if not currentUser:
        raise HTTPException(404, detail={"Error":"User not found"})
    data = body.model_dump()
    for k,v in data.items():
        setattr(currentUser, k, v)
    db.commit()
    db.refresh(currentUser)

    return {"Status ":"User updated successfully",
            "User details ":currentUser
            }

def deleteUser(db:Session, user:User):
    currentUser = db.query(User).filter(User.id == user.id).first()
    if not currentUser:
        raise HTTPException(404, detail={"Error":"User not found"})

    db.delete(currentUser)
    db.commit()

    return {"Status":"User deleted successfully"}

def createUserProfile(body:ProfileSchema, db:Session, user:User):
    currentUser = db.query(User).filter(User.id == user.id).first()
    if currentUser.profile:
        raise HTTPException(404, detail={"Error":"User already have a profile"})
    if not currentUser:
        raise HTTPException(404, detail={"Error":"User not found"})
    userProfile = Profile(**body.model_dump(), user_id = user.id)
    db.add(userProfile)
    db.commit()
    db.refresh(userProfile)

    return {"Status":"User profile created successfully"}

def updateUserProfile(body:ProfileSchema, db:Session, user:Profile):
    userProfile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not userProfile:
        raise HTTPException(404, detail={"Error":"User's profile is not created right now."})
    data = body.model_dump()
    for k,v in data.items():
        setattr(userProfile, k, v)
    db.commit()
    db.refresh(userProfile)

    return {"Status ":"User's profile updated successfully",
            "User details ":userProfile
            }