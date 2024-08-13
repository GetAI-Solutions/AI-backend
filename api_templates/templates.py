from pydantic import BaseModel

class SignUp(BaseModel):
    email: str = "oadeniran82@gmail.com"
    user_name: str = "oade"
    password: str = "test_password"
    phone_no: str = "+2348097219648"
    country: str = "Nigeria"
    preferred_language: str = "EN"

class LogIN(BaseModel):
    email: str = "oadeniran82@gmail.com"
    password: str = "test_password"
    login_type: str = "email"
    phone_no: str = "+2348097219648" 

class chatTemp(BaseModel):
    userID: str = "id"
    prod_id:str = "product_barcode"
    product_full_details: str = "full_details"
    user_message:str = "user_message"