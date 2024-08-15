from pydantic import BaseModel

language_code = {"en" : "English",
                 "fr" : "French",
                 "sw" : "Swahili"}

class SignUp(BaseModel):
    email: str = "oadeniran82@gmail.com"
    user_name: str = "oade"
    password: str = "test_password"
    phone_no: str = "+2348097219648"
    country: str = "Nigeria"
    preferred_language: str = "En"

class LogIN(BaseModel):
    email: str = "oadeniran82@gmail.com"
    password: str = "test_password"
    login_type: str = "email"
    phone_no: str = "+2348097219648" 

class chatTemp(BaseModel):
    userID: str = "id"
    bar_code:str = "product_barcode"
    user_message:str = "user_message"