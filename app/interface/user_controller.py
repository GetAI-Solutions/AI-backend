from ..application import user_service
import random
from config import g_app_password
from ..schema_templates.templates import SignUp, LogIN, UpdateProfile

async def signup(payload: SignUp):
    print(payload)
    try:
        details = await user_service.check_user_exists(payload.email.lower())
    except Exception as e:
        print(e)
        return "Error with DB"
    if type(details) != str and details is not None:
        print("Here")
        return "Email is registered already"
    try:
        details = await user_service.create_user(payload)
        if type(details) == str:
            return details
        else:
            details = details[1]
    except Exception as e:
        print(e)
        return "Error with user history creation"
    if type(details) != str:
        hh = await user_service.create_user_history(str(details.inserted_id))
        if hh != None:
            return hh
    return "success"


async def send_otp(email : str):
    otp = random.randint(100000, 999999)
    try:
        await user_service.send_otp_mail(email, g_app_password, str(otp))
    except Exception as e:
        print(str(e))
        return "Error sending otp"
    
    return "success", {"otp" : otp}

async def login(payload: LogIN):
    try:
        # Fetch user based on login type
        if payload.login_type == "email":
            user_details = await user_service.find_user_by_email(payload.email)
        elif payload.login_type == "phone":
            user_details = await user_service.find_user_by_phone(payload.phone_no)
        else:
            return "Invalid login type"
        
        # Validate user credentials
        user_data = await user_service.validate_user(user_details, payload.password)
        if type(user_data) != str:
            return {"status": "success", "data": user_data}
        else:
            return user_data
        
    except Exception as e:
        print(str(e))
        return "Error in user login"
    


async def get_user_product_history(ID: str):
    try:
        u_h = await user_service.get_user_history(ID)
    except:
        return "Error getting user history"
    
    return u_h

async def get_user_chat_history(userID: str, barcode:str):
    try:
        u_h = await user_service.get_user_chat_history(userID, barcode)
    except:
        return "Error getting user history"
    
    return u_h

async def update_user_details(update_details : UpdateProfile):
    # Step 1: Fetch user details to verify if the user exists
    user_d = await user_service.find_user_by_id(update_details.user_id)
    if type(user_d) == str:
        print("HEre")
        return user_d
    else:
        update_data = {key: value for key, value in dict(update_details).items() if value is not None and key != "user_id"}
        if not update_data:
            return "No valid fields provided for update"
    
        return await user_service.update_user_details(update_details.user_id, update_data)
    

async def give_user_feedback(userID:str, feedback:str, product_name:str = None):
    try:
        return await user_service.give_user_feedback(userID, feedback, product_name)
    except:
        return  "Unknown Error"

