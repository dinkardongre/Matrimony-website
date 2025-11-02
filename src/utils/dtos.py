from pydantic import BaseModel
from datetime import date

class UserSchema(BaseModel):
    name : str
    gender : str
    email : str
    phone : str
    username : str
    password : str
    date_of_birth : date
    is_active : bool

class LoginSchema(BaseModel):
    username : str
    password : str

class UpdatePasswordSchema(BaseModel):
    old_password : str
    new_password : str

class ForgetPasswordSchema(BaseModel):
    email : str

class VerifyOtpSchema(BaseModel):
    email : str
    otp : str
    new_password : str
    
class ProfileSchema(BaseModel):
    religion : str
    caste : str
    occupation : str
    education : str
    city : str
    bio : str
    photo_url : str