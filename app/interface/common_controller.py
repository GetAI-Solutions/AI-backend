from fastapi import UploadFile
from io import BytesIO
from PIL import Image
from ..application import barcode_service, bot_service , product_service, user_service
from config import OAI_KEY_TOKEN
from ..schema_templates.templates import language_code, chatTemp
from ..infrastructure.external.perplexity_sourcing import get_details_from_perplexity

async def upload_barcode(file: UploadFile):
    file_contents = await file.read()
    img = BytesIO(file_contents)
    pi_img = Image.open(img)
    boundary_img, res = await barcode_service.scan_barcode_from_image(pi_img)
    if res:
        extracted_barcode = res[0].data.decode("utf-8")
    else:
        return "No barcode detected"
    
    return "success", {"product_barcode": extracted_barcode.lstrip('0')}

async def get_product_details(barcode: str, perplexity = False):
    try:
        product = await product_service.find_product_by_barcode(barcode, perplexity)
        if not product:
            return "Product not found"
        return product
    except Exception as e:
        print(e)
        return "Error fetching product details"


async def get_user_preferred_language(user_id: str):
    try:
        user = await user_service.find_user_by_id(user_id)
        if not user:
            return "User not found"
        return "language", language_code.get(user["preferred_language"].lower(), "English") 
    except Exception as e:
        print(e)
        return "Error in getting details"

async def get_chat_response(product_details: str, user_message: str, user_pref_language: str):
    sys_msg = await bot_service.get_sys_msgs(product_details, pref_lang=user_pref_language)
    try:
        model_resp = await bot_service.get_model_resp(sys_msg, text=user_message)
    except Exception as e:
        print(e)
        return "Error generating model response"
    try:
        response = model_resp.choices[0].message.content
        return "success", response
    except:
        return response
    

async def add_conversation_to_history(conv: dict, user_id: str, barcode: str):
    try:
        return await user_service.add_to_user_chat_hist(conv, user_id=user_id, prod_id=barcode)
    except Exception as e:
        print(e)
        return "Error adding conversation to history"

async def chat_with_model(payload: chatTemp):
    # Step 1: Get product details
    product = await get_product_details(payload.bar_code, perplexity = payload.perplexity)
    if type(product) == str:
        return product

    # Step 2: Get user's preferred language
    user_pref_language = await get_user_preferred_language(payload.userID)
    if type(user_pref_language) == str:
        return user_pref_language

    # Step 3: Get the model response
    response = await get_chat_response(product["product_details"], payload.user_message, user_pref_language[1])
    if type(response) == str:
        return response 

    # Step 4: Add the conversation to history
    conversation = {
        "user_message": payload.user_message,
        "model_resp": response[1]
    }
    resp = await add_conversation_to_history(conversation, user_id=payload.userID, barcode=payload.bar_code)
    if type(resp) == str:
        return resp
    
    return "success", {
        "user_message": payload.user_message,
        "model_resp": response
    }

async def source_details_from_perplexity(product_name:str, bar_code: str):
    try:
        details = get_details_from_perplexity(product_name, bar_code)
    except Exception as e:
        return "Error from perplexity"
    return "success", details
    
async def save_details_from_perplexity(prod_name, bar_code, details):
    try:
        res = await product_service.add_product_to_perplexity_db(prod_name, bar_code, details)
    except Exception as e:
        return "Error adding details to perplexity DB" + str(e)
    
    if type(res) == str:
        return res
    else:
        return {
            "response" : details
        }

async def product_from_perplexity(prod_name:str, bar_code: str):
    try:
        details = await source_details_from_perplexity(prod_name, bar_code)
    except Exception as e:
        return "Error getting details from perplexity" + str(e)
    
    if type(details) != str:
        try:
            res = await save_details_from_perplexity(prod_name, bar_code, details[1])
        except Exception as e:
            return "Error getting details from perplexity" + str(e)
        if type(res) != str:
            return {
                "response" : details
            }
        else:
            return res
    else:
        return details
