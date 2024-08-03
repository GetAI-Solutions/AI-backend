from pydantic import BaseModel

class SignUp(BaseModel):
    email: str = "oadeniran82@gmail.com"
    user_name: str = "oade"
    password: str = "test_password"

class LogIN(BaseModel):
    email: str = "oadeniran82@gmail.com"
    password: str = "test_password"