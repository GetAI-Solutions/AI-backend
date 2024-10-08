from fastapi import File, UploadFile
from ..application import product_service, bot_service, user_service
from ..schema_templates.templates import language_code
from config import OAI_KEY_TOKEN
import random

async def get_product(bar_code: str):
    product = await product_service.find_product_by_barcode(bar_code)
    if product:
        return "success", {
            "_id": str(product["_id"]),
            "product_code": product["product_code"],
            "product_name": product["product_name"],
            "product_details": product["product_details"]
        }
    else:
        return "Product not found"

async def get_products_by_name(product_name: str):
    try:
        product = await product_service.find_products_by_name(product_name)
        if product:
            return "success", product
        else:
            return "Product not found"
    except Exception as e:
        return "Error with DB in finding product \n"

async def get_product_summary(bar_code: str, userID: str):
    am = False
    try:
        product = await product_service.find_product_by_barcode(bar_code)
        if not product:
            return "product not found"
    except Exception as e:
        return "Error with DB in finding product \n"
    
    try:
        user = await user_service.find_user_by_id(userID)
        if user:
            user_pref_language = user["preferred_language"]
            user_pref_language = language_code[user_pref_language.lower()]
        else:
            return "user not found"
    except:
        return "Some error"

    if product:
        try:
            resp = await user_service.add_to_user_product_hist(prod_code=bar_code, user_id=str(userID))
            if type(resp) == str:
                return resp
        except Exception as e:
            print(str(e))
            return "Error in adding product to user history"
        
        details = product["product_details"]

        name = product["product_name"]
        barcode = product["product_code"]

        img_url = ""

        if "img_url" in product:
            img_url = product["img_url"]
         
        sys_msg_summary = await bot_service.get_sys_msgs_summary(details, pref_lang=user_pref_language)
        
        try:
            if user_pref_language.lower() == "am":
                am = True
            summary_txt = await bot_service.get_model_resp(sys_msg_summary, am = am)
        except Exception as e:
            return "Error in getting summary with OAI wrapper"

        try:
            summ_cont = summary_txt.choices[0].message.content
        except:
            return summ_cont

        return "success", {
            "product": {
                "product_barcode" : barcode,
                "product_name" : name,
                "product_summary": summ_cont,
                "image_url" : img_url
            }
        }
    else:
        try:
            await product_service.add_product_to_not_found_db(bar_code)
        except Exception as e:
            print(str(e))

        return "Product not found"
    
async def add_product_to_db(file: UploadFile, product_code: str, product_name: str):
    # Read and validate product details from the uploaded file
    product_details = await product_service.read_product_file(file)
    
    if len(product_details) <= 10:
        return "Product details are too short"
    
    # Check if the product already exists in the database
    existing_product = await product_service.check_product_exists(product_code)
    if existing_product:
        return "Product already exists in the database"
    
    # Add the product to the database
    res = await product_service.add_product(product_code, product_name, product_details)
    return res 

async def get_all_products(option):
    try:
        all_products = await product_service.get_all_products(option)
    except:
        return "unknown error"
    
    return all_products


async def add_img_to_product(file: UploadFile, bar_code: str):
    try:
        details = await product_service.find_product_by_barcode(bar_code)
    except Exception as e:
        raise "Unknow Error"
    if type(details) != str:
        p_db_id = str(details["_id"])
        try:
            resp = await product_service.add_img_to_product(file, bar_code, p_db_id)
        except Exception as e:
            return "Uknown Error" + str(e)
    
    return resp

def split_list_into_three(lst):
    n = len(lst)
    
    # Calculate the size of each part
    split_size = n // 3
    remainder = n % 3
    
    # Calculate the start indices for each split
    first_split_end = split_size + (1 if remainder > 0 else 0)
    second_split_end = first_split_end + split_size + (1 if remainder > 1 else 0)
    
    # Create the three parts
    part1 = lst[:first_split_end]
    part2 = lst[first_split_end:second_split_end]
    part3 = lst[second_split_end:]
    
    return part1, part2, part3

async def get_home_page_products():
    try:
        products = await product_service.find_products_with_non_empty_imgfield()
    except Exception as e:
        return "Error with db"
    
    try:
        africanProducts = await product_service.find_products_by_barcodes([8719327078297, 4005808226740, 6186000077021])
    except Exception as e:
        return "Error with db"
    
    split1, split2, split3= split_list_into_three(products)
    response = [
        {"section":"African Made",
        "items": africanProducts},
        {"section":"Popular Today",
        "items": random.sample(split1, 3)},
        {"section":"Sponsored",
        "items": random.sample(split2, 3)},
        {"section":"Latest Additions",
        "items": random.sample(split3, 3)},
    ]

    #print(response)
    
    return response

async def rate_product(product_code, rating):
    try:
        resp = await product_service.rate_product(product_code, rating)
    except Exception as e:
        return "Error with db"
    
    if type(resp) == str:
        return resp
    
    return "success", resp