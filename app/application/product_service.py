from typing import Optional
from fastapi import HTTPException
from ..infrastructure.database.db import productsClient, noProductClient, alternative_details
from fastapi import File, UploadFile
from config import contClient, load_blob
from io import BytesIO
from bson.objectid import ObjectId

async def find_product_by_barcode(bar_code: str, perplexity = False) -> Optional[dict]:
    if perplexity == False:
        try:
            product = productsClient.find_one({"product_code": int(bar_code)})
            return product
        except Exception as e:
            return "Error with DB"
    else:
        try:
            product = alternative_details.find_one({"product_code": int(bar_code)})
            return product
        except Exception as e:
            return "Error with DB"


async def add_product_to_not_found_db(bar_code: str):    
    try:
        noProductClient.insert_one({
            "product_code" : bar_code
        })
    except Exception as e:
                print(str(e))

async def add_product_to_perplexity_db(product_name, bar_code, details):
    try:
        return alternative_details.insert_one({
            "product_name" : product_name,
            "product_code" : bar_code,
            "product_details" : details
        })
    except Exception as e:
        print(str(e))
        return "Could not add to perplexity"

async def read_product_file(file: UploadFile) -> str:
    try:
        prod_details = await file.read()
        prod_details = prod_details.decode("utf-8")
        return prod_details
    except Exception as e:
        print(e)
        return "Error reading the file"

async def check_product_exists(product_code: str):
    try:
        existing_product = productsClient.find_one({'product_code': int(product_code)})
        return existing_product
    except Exception as e:
        print(e)
        return "Database query failed"

async def add_product(product_code: str, product_name: str, product_details: str):
    try:
        product_data = {
            "product_code": int(product_code),
            "product_name": product_name,
            "product_details": product_details
        }
        productsClient.insert_one(product_data)
        return {"msg": "Product added successfully"}
    except Exception as e:
        print(e)
        return "Product could not be added, please try again" + str(e)

async def get_all_products(option  = "inBD"):
    if option == "InDB":
        try:
            all_products = productsClient.find()
            if all_products:
                products_l = {p["product_code"] : p["product_name"] for p in all_products} 
                no_of_products = len(products_l)

                return {
                    "Number of products" : no_of_products,
                    "all_barcodes" : products_l
                }
        except:
            return "Error with db"
    elif option == "notInDB":
        try:
            all_products = noProductClient.find()
        except Exception as e:
            return "Error with db"
        if all_products:
            products_l = [p["product_code"] for p in all_products]
            no_of_products = len(products_l)

            return {
                "Number of products" : no_of_products,
                "all_barcodes" : products_l
            }
    elif option == "perplexity":
        try:
            all_products = alternative_details.find()
        except Exception as e:
            return "Error in Db"
        
        if all_products:
                products_l = {p["product_code"] : p["product_name"] for p in all_products} 
                no_of_products = len(products_l)

                return {
                    "Number of products" : no_of_products,
                    "all_barcodes" : products_l
                }
    elif option == "NoIMG":
        try:
            all_products = productsClient.find()
        except:
            return "Error with db"
        
        if all_products:
            products_l = {p["product_code"] : p["product_name"] for p in all_products if "img_url" not in p}
            return products_l
    else:
        return "Option not recognized"
    
async def add_img_to_product(file: UploadFile, bar_code: str, p_db_id:str):
    try:
        blob = load_blob(contClient, bar_code + ".png")
        file_contents = await file.read()
        img = BytesIO(file_contents)
        blob.upload_blob(img, overwrite = True)
        blob_url = blob.url
    except Exception as e:
        return "Error in uploading file to blob" 
    
    try:
        productsClient.find_one_and_update({"_id":ObjectId(p_db_id)}, {"$set" : {"img_url" : blob_url}})
    except:
        return "Error with Db in updating product url"
    
    return {
        "response" : "Image Added"
    }