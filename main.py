import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from io import BytesIO
from PIL import Image
import pymongo
import json
import yagmail
import random
from bson.objectid import ObjectId

from api_templates.templates import SignUp, LogIN, chatTemp, language_code
from helpers.helper import scan_barcode_from_image, get_sys_msgs, get_sys_msgs_summary, get_resp, add_to_user_product_hist, send_otp_mail, add_to_user_chat_hist

## Load environment variables from .env file
load_dotenv()
appENV = os.getenv("APP_ENV", "local")
OAI_KEY = os.getenv("OAI_KEY", "local")
DATABASE_URI = os.getenv("DATABASE_URI", "local")
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")
g_app_password = os.getenv("G_APP_PASSWORD")
OAI_KEY_TOKEN = os.getenv("OAI_KEY_TOKEN", "local")

## Initialize MongoDB client and databases
DBClient = pymongo.MongoClient(DATABASE_URI)
dbClient = DBClient["getAIDB"]
usersClient = dbClient["users"]
productsClient = dbClient["products"]
usersHistoryClient = dbClient["user_history"]
userFeedbackClient = dbClient["user_feedback"]
noProductClient = dbClient["product_not_found"]

## Initialize OpenAI client
client = OpenAI(api_key=OAI_KEY)

## Define API prefix based on environment
if appENV != "local":
    prefix = "/get-ai-service"
else:
    prefix = "/get-ai"

## Set API documentation details
title = f"get-ai API for {appENV} Environment"
description = f"get-ai API for {appENV} Documentation"

tags_metadata = [
    {
        "name": "get AI",
        "description": "Endpoints to power get-ai",
    }
]

## Initialize FastAPI app
app = FastAPI(
    docs_url=prefix + "/dev/documentation",
    openapi_url=prefix + "/openapi.json",
    title=title,
    description=description,
    openapi_tags=tags_metadata,
)

## Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Define root endpoint
@app.get(f"{prefix}/")
async def root():
    return "Hello World - Welcome to get-ai service"

## Define endpoint for user signup
@app.post(f"{prefix}/signup")
async def signup(payload: SignUp):
    print(payload)
    try:
        details = usersClient.find_one({"email": payload.email})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=402, detail="Error in signup with DB, please try again")
    if details:
        raise HTTPException(status_code=400, detail="Email is registered already")
    try:
        details = usersClient.insert_one(dict(payload))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=402, detail="Error in signup with DB, please try again")
    usersHistoryClient.insert_one({
        "uid" : str(details.inserted_id),
        "product_history" : [],
        "chat_history" : {}
    })
    return {
        
        "message": "Sign Up successful",
        "status_code": 200
    }

## Define endpoint for OTP sending
@app.post(f"{prefix}/send-otp")
async def send_otp(email : str = Form(...)):
    otp = random.randint(100000, 999999)
    try:
        send_otp_mail(email, g_app_password, str(otp))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail="Error sending otp")
    
    return {"otp" : otp}


## Define endpoint for user login
@app.post(f"{prefix}/login")
async def login(payload: LogIN):
    try:
        if payload.login_type == "email":
            details = usersClient.find_one({"email": payload.email})
        elif payload.login_type == "phone":
            details = usersClient.find_one({"phone_no": payload.phone_no})
    except:
        raise HTTPException(status_code=402, detail="Error in login with DB, please try again")
    
    if details:
        print(str(details["_id"]))
        if details["password"] == payload.password:
            try: 
                return {
                    "message": "Sign In successful",
                    "uid": str(details["_id"]),
                    "user_name": details["user_name"],
                    "email": details["email"],
                    "phone_no": details["phone_no"],
                    "country": details["country"],
                    "preferred_language": details["preferred_language"]
                }
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail="Wrong Password")
    else:
        raise HTTPException(status_code=404, detail="User not found")

## Define endpoint for uploading a barcode image
@app.post(f"{prefix}/upload-barcode")
async def upload_barcode(file: UploadFile = File(...), id: str = Form(...)):
    file_contents = await file.read()
    img = BytesIO(file_contents)
    pi_img = Image.open(img)
    boundary_img, res = scan_barcode_from_image(pi_img)
    if res:
        extracted_barcode = res[0].data.decode("utf-8")
    else:
        raise HTTPException(status_code=404, detail="No barcode detected")
    
    return {"product_barcode": extracted_barcode.lstrip('0')}

## Define endpoint for retrieving product details
@app.post(f"{prefix}/get-product")
async def get_product(bar_code: str = Form(...), user_id: str = Form(...)):
    try:
        product = productsClient.find_one({"product_code": int(bar_code)})
    except:
        raise HTTPException(status_code=402, detail="Error with DB")
    if product:
        try:
            add_to_user_product_hist(prod_code=bar_code, user_id=str(user_id), uh_client=usersHistoryClient)
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=400, detail = "user not found!")
        return {
            "_id": str(product["_id"]),
            "product_code": product["product_code"],
            "product_name": product["product_name"],
            "product_details": product["product_details"]
        }
    else:
        raise HTTPException(status_code=404, detail="Product not found")

## Define endpoint for retrieving product summary
@app.post(f"{prefix}/get-product-summary")
async def get_product_summary(bar_code: str = Form(...), userID: str = Form(...)):
    try:
        product = productsClient.find_one({"product_code": int(bar_code)})
    except:
        raise HTTPException(status_code=402, detail="Error with DB")
    
    try:
        user_pref_language = usersClient.find_one({"_id":ObjectId(userID)})["preferred_language"]
        user_pref_language = language_code[user_pref_language.lower()]
    except:
        raise HTTPException(status_code="400", detail="user not found")
    

    if product:
        details = product["product_details"]
        name = product["product_name"]

        sys_msg_summary = get_sys_msgs_summary(details)
        
        try:
            summary_txt = get_resp(sys_msg_summary, pref_lang= user_pref_language, token= OAI_KEY_TOKEN)
        except Exception as e:
            raise HTTPException(status_code=405, detail="Error in getting summary with OAI wrapper")

        try:
            summ_cont = summary_txt["response"]["messages"][0]["content"]
        except:
            raise HTTPException(status_code=400, detail=summary_txt)

        return {
            "product": {
                "product_name" : name,
                "product_summary": summ_cont,
                "image_url" : "soon"
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Product not found")

## Define endpoint for adding a new product
@app.post(f"{prefix}/add-product")
async def add_product(file: UploadFile = File(...), product_code: str = Form(...), product_name: str = Form(...)):
    try:
        prod_details = await file.read()
        print(prod_details.decode("utf-8"))
        prod_details = prod_details.decode("utf-8")
    except:
        raise HTTPException(status_code=402, detail="Error with file")
    print(len(prod_details))
    if len(prod_details) > 10:
        try:
            existingdetails = productsClient.find_one({'product_code' : int(product_code)})
        except:
            raise HTTPException(status_code=400, detail="Product could not be added, try again")
        if existingdetails:
            raise HTTPException(status_code=400, detail="Product already in DB, try another product")
        else:
            try:
                dets = {
                    "product_code": int(product_code),
                    "product_name": product_name,
                    "product_details": prod_details
                }
                productsClient.insert_one(dets)
                return {"msg": "Product added"}
            except:
                raise HTTPException(status_code=400, detail="Product could not be added, try again")
    else:
        raise HTTPException(status_code=400, detail="Product details too short")

## Define endpoint for retrieving user product history
@app.post(f"{prefix}/get-user-product-history")
def get_user_history(ID: str = Form(...)):
    try:
        u_h = usersHistoryClient.find_one({"uid": ID})
    except:
        raise HTTPException(status_code=404, detail="User history not found")
    
    if u_h:
        return {'product_history': u_h["product_history"]}

## Define endpoint for retrieving user chat history
@app.post(f"{prefix}/get-user-chat-history")
def get_user_history(userID: str = Form(...), barcode: str = Form(...)):
    try:
        u_h = usersHistoryClient.find_one({"uid": userID})
    except:
        raise HTTPException(status_code=404, detail="User history not found")
    
    if u_h:
        if barcode in u_h["chat_history"]:

            return  {"chat_history" : u_h["chat_history"][barcode]}
        else:
            return {
                "chat_history" : []
            }
    else:
        raise HTTPException(status_code=404, detail="User history not found")

## Define endpoint chatting
@app.post(f"{prefix}/chat")
def chat_with_model(payload : chatTemp):
    try:
        product = productsClient.find_one({"product_code": int(payload.bar_code)})
    except:
        raise HTTPException(status_code="400", detail="product not found")
    
    try:
        user_pref_language = usersClient.find_one({"_id":ObjectId(payload.userID)})["preferred_language"]
        user_pref_language = language_code[user_pref_language.lower()]
    except:
        raise HTTPException(status_code="400", detail="user not found")

    sys_msg = get_sys_msgs(product["product_details"])

    try:

        model_resp = get_resp(sys_msg, text= payload.user_message, pref_lang= user_pref_language, token= OAI_KEY_TOKEN)

    except Exception as e:
        raise HTTPException(status_code=405, detail="Error in getting response with OAI wrapper")

    try:
        response = model_resp["response"]["messages"][0]["content"]

    except:
        raise HTTPException(status_code=400, detail=model_resp)
    
    conv = {
        "user_message" : payload.user_message,
        "model_resp": response
    }

    try:
        add_to_user_chat_hist(conv, user_id=payload.userID, prod_id = payload.bar_code, uh_client=usersHistoryClient)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail="Error adding conversation to history")
    return {
        "user_message" : payload.user_message,
        "model_resp": response
    }

## Define endpoint to update user preferred language
@app.patch(f"{prefix}/update-preferred-language")
def update_preferred_language(userID:str = Form(...), preferred_language: str = Form(...)):
    if preferred_language.lower() not in language_code.keys():
        raise HTTPException(status_code=400, detail="Preferred language must be one of [EN, FR, SW]")
    else:

        try:
            user_det = usersClient.find_one({"_id":ObjectId(userID)})
        except:
            raise HTTPException(status_code=400, detail="user not found") 
        
        #print(user_det)
        
        if user_det:
            try:
                usersClient.find_one_and_update({"_id":ObjectId(userID)}, {"$set" : {"preferred_language" : preferred_language.lower()}})
            except:
                raise HTTPException(status_code=400, detail="Error with Db in updating language preference")
            
            return {
                "message" : "Language preference update success"
            }
        else:
            raise HTTPException(status_code=400, detail="user not found") 


@app.get(f"{prefix}/get-all-products")
def get_all_products():
    try:
        all_products = productsClient.find()
    except:
        raise HTTPException(status_code=400, detail="Error with db")
    
    if all_products:
        products_l = [p["product_code"] for p in all_products]
        no_of_products = len(products_l)

        return {
            "Number of products" : no_of_products,
            "all_barcodes" : products_l
        }

@app.post(f"{prefix}/give-user-feedback")
def give_user_feedback(userID:str = Form(...), feedback:str = Form(...)):
    try:
        userFeedbackClient.insert_one({"uid" : userID,
                                       "feedback" : feedback})
    except:
        raise HTTPException(status_code=400, detail= "Error with db in adding feedback")
    
    return {
        "response" : "feedback succesfully added"
    }


