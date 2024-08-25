from fastapi import APIRouter, HTTPException, Form
from ..interface import user_controller
from ..schema_templates.templates import SignUp, LogIN, UpdateProfile


router = APIRouter()

@router.post("/signup")
async def signup(payload: SignUp):

    res = await user_controller.signup(payload)
    if res == "success":
        return {
            
            "message": "Sign Up successful",
            "status_code": 200
        }
    else:
        raise HTTPException(status_code=400, detail=res)

## Define endpoint for OTP sending
@router.post(f"/send-otp")
async def send_otp(email : str = Form(...)):
    res = await user_controller.send_otp(email)
    if type(res) == str:
        raise HTTPException(status_code=400, detail=res)
    else:
        return res[1]


## Define endpoint for user login
@router.post(f"/login")
async def login(payload: LogIN):
    res = await user_controller.login(payload)
    if type(res) == str:
        raise HTTPException(status_code=400, detail=res)
    else:
        return res["data"]

## Define endpoint for retrieving user product history
@router.post(f"/get-user-product-history")
async def get_user_product_history(ID: str = Form(...)):
    try:
        u_h = await user_controller.get_user_product_history(ID)
    except:
        raise HTTPException(status_code=404, detail="Error with user history")
    
    if type(u_h) == str:
        raise HTTPException(status_code=404, detail="Error with user history")
    else:
        return u_h

## Define endpoint for retrieving user chat history
@router.post(f"/get-user-chat-history")
async def get_user_history(userID: str = Form(...), barcode: str = Form(...)):
    try:
        u_h = await user_controller.get_user_chat_history(userID, barcode)
    except:
        raise HTTPException(status_code=404, detail="Error with user history")
    
    if type(u_h) == str:
        raise HTTPException(status_code=404, detail="Error with user history")
    else:
        return u_h

## Define endpoint to update user preference
@router.patch(f"/update-user-preference")
async def update_user_pref(update_details: UpdateProfile):
    try:
        user_det = await user_controller.update_user_details(update_details)
    except:
        raise HTTPException(status_code=400, detail="Error Updating preference ") 
    
    if type(user_det) == str:
        raise HTTPException(status_code=400, detail="Error Updating preference " + user_det) 
    else:
        return user_det

## Define endpoint to update user preference   
@router.post(f"/give-user-feedback")
async def give_user_feedback(userID:str = Form(...), feedback:str = Form(...), product_name:str = None):
    try:
        resp = await user_controller.give_user_feedback(userID, feedback, product_name)
    except:
        raise HTTPException(status_code=400, detail= "Error with db in adding feedback")
    
    if type(resp) == str:
        raise HTTPException(status_code=400, detail= resp)
    
    return resp
