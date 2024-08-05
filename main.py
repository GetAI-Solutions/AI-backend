import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from openai import OpenAI
from io import BytesIO
from PIL import Image
import pymongo
import json
import yagmail


from api_templates.templates import SignUp, LogIN

from helpers.helper import scan_barcode_from_image, get_sys_msgs, get_sys_msgs_summary, get_resp



## Load envs
load_dotenv()
appENV = os.getenv("APP_ENV", "local")
OAI_KEY= os.getenv("OAI_KEY", "local")
DATABASE_URI = os.getenv("DATABASE_URI", "local")

#DB INFO
DBClient = pymongo.MongoClient(DATABASE_URI)
dbClient = DBClient["getAIDB"]
usersClient = dbClient["users"]
productsClient = dbClient["products"]

client = OpenAI(
    # This is the default and can be omitted
    api_key=OAI_KEY,
)

if appENV != "local":
    prefix = "/get-ai-service"
else:
    prefix = "/get-ai"

title = f"get-ai API for {appENV} Environment"
description = f"get-ai api for {appENV} Documentation"


tags_metadata = [
    {
        "name": "get AI",
        "description": "Endpoints to power get-ai",
    }
]

app = FastAPI(
    docs_url= prefix + "/dev/documentation",
    openapi_url=prefix + "/openapi.json",
    title=title,
    description=description,
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(f"{prefix}/")
async def root():
    return "Hello World - Welcome to get-ai service"

@app.post(f"{prefix}/send-otp")
def send_otp(email: str = Form(...)):
    yag = yagmail.SMTP("getaicompany@gmail.com", "Disposable12345@")
    otp = ""
    yag.send(subject="Great!")

@app.post(f"{prefix}/signup")
async def signup(payload: SignUp):
    print(payload)
    try:
        details = usersClient.find_one({"email" : payload.email})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=402, detail="Error in signup with db, please try again")
    if details:
            raise HTTPException(status_code=400, detail="Email is registered already")
    try:
        usersClient.insert_one(dict(payload))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=402, detail="Error in signup with db, please try again")
    
    return {
    "message" : "Sign Up successful",
    "status_code" : 200}
    

@app.post(f"{prefix}/login")
async def login(payload: LogIN):
    try:
        if payload.login_type == "email":
            details = usersClient.find_one({"email" : payload.email})
        elif payload.login_type == "phone":
            details = usersClient.find_one({"phone_no" : payload.phone_no})
    except:
        raise HTTPException(status_code=402, detail="Error in signup with db, please try again")
    
    if details:
        print(str(details["_id"]))
        if details["password"] == payload.password:
            return {
                    "message" : "Sign In successful",
                    "uid" : str(details["_id"])
                    }
        else:
            raise HTTPException(status_code=400, detail="Wrong Password")
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post(f"{prefix}/upload-barcode")
async def upload_barcode(file: UploadFile = File(...), id: str = Form(...)):
    file_contents = await file.read()
    img =  BytesIO(file_contents)
    pi_img = Image.open(img)
    boundary_img, res = scan_barcode_from_image(pi_img)
    if res:
        extracted_barcode = res[0].data.decode("utf-8")
    else:
        raise HTTPException(status_code=404, detail="No barcode detected")
    
    return {"product_id" : extracted_barcode.lstrip('0')}

@app.post(f"{prefix}/get-product")
async def get_product(bar_code: str = Form(...)):
    try:
        product = productsClient.find_one({"product_code" : int(bar_code)})
    except:
        raise HTTPException(status_code=402, detail="Error with DB")
    if product:
        return {
            "_id" : str(product["_id"]),
            "product_code": product["product_code"],
            "product_name" : product["product_name"],
            "product_details" : product["details"]
        }
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.post(f"{prefix}/get-product-summary")
async def get_product_summary(bar_code: str = Form(...)):
    try:
        product = productsClient.find_one({"product_code" : int(bar_code)})
    except:
        raise HTTPException(status_code=402, detail="Error with DB")
    if product:
        details = product["details"]
        sys_msg_summary = get_sys_msgs_summary(details)

        summary_txt = get_resp(client, sys_msg_summary, "", summary=True)

        print(summary_txt)

        return{
            "product_summary" : summary_txt
        }
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.post(f"{prefix}/add-product")
async def add_product(file: UploadFile = File(...), id: str = Form(...), product_name: str = Form(...)):
    try:
        prod_details = await file.read()
        print(prod_details.decode("utf-8"))
    except:
        raise HTTPException(status_code=402, detail="Error with file")
    if len(prod_details) < 10:
        try:
            dets = {
                "product_code": id,
                "product_name" : product_name,
                "product_details" : prod_details
            }
            productsClient.insert_one(dets)
            return dets
        except:
            raise HTTPException(status_code=400, detail="Product could not be added try again")
    else:
        raise HTTPException(status_code=400, detail="Product details too short")
