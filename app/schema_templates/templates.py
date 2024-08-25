from pydantic import BaseModel
from typing import Optional

language_code = {"en" : "English",
                 "fr" : "French",
                 "sw" : "Swahili",
                 "hu" : "Hausa",
                 "om" : "Oromo",
                 "am" : "Amharic",
                 "zu" : "Zulu",
                 "twi" : "Twi"}

class SignUp(BaseModel):
    email: str = "oadeniran82@gmail.com"
    user_name: str = "oade"
    password: str = "test_password"
    phone_no: str = "+2348097219648"
    country: str = "Nigeria"
    preferred_language: str = "En"

class UpdateProfile(BaseModel):
    user_id : Optional[str] = None
    email: Optional[str] = None
    user_name: Optional[str] = None
    password: Optional[str] = None
    phone_no: Optional[str] = None
    country: Optional[str] = None
    preferred_language: Optional[str] = None

class LogIN(BaseModel):
    email: str = "oadeniran82@gmail.com"
    password: str = "test_password"
    login_type: str = "email"
    phone_no: str = "+2348097219648" 

class chatTemp(BaseModel):
    userID: str = "id"
    bar_code:str = "product_barcode"
    user_message:str = "user_message"
    perplexity: bool = False