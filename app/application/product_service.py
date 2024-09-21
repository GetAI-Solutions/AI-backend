from typing import Optional
from fastapi import HTTPException
from ..infrastructure.database.db import productsClient, noProductClient, alternative_details, alternative_details_uuid
from fastapi import File, UploadFile
from config import contClient, load_blob
from azure.storage.blob import ContentSettings
from io import BytesIO
from bson.objectid import ObjectId

async def find_product_by_barcode(bar_code: str, perplexity = False, noCode = False, userID = None) -> Optional[dict]:
    if perplexity == False:
        try:
            product = productsClient.find_one({"product_code": int(bar_code)})
            return product
        except Exception as e:
            return "Error with DB"
    else:
        if perplexity == True and noCode == False:
            try:
                product = alternative_details.find_one({"product_code": int(bar_code), "userID": userID})
                return product
            except Exception as e:
                return "Error with DB"
        else:
            try:
                product = alternative_details_uuid.find_one({"product_code": bar_code, "userID": userID})
                return product
            except Exception as e:
                return "Error with DB"

async def find_products_by_name(product_name: str):
    try:
        product = {p["product_name"] : p["product_code"] for p in productsClient.find({"product_name_lower": {"$regex": product_name.lower()}})}
        return product
    except Exception as e:
        return "Error with DB"

async def add_product_to_not_found_db(bar_code: str):    
    try:
        noProductClient.insert_one({
            "product_code" : int(bar_code)
        })
    except Exception as e:
                print(str(e))

async def add_product_to_perplexity_db(product_name, bar_code, details, userID):
    try:
        check_product_exists = alternative_details.find_one({'product_code': int(bar_code), "userID": userID})
        if check_product_exists:
            return alternative_details.find_one_and_update({'product_code': int(bar_code), "userID": userID}, {"$set" : {"product_details" : details}})
    except Exception as e:
        print(e)
        return 'Database query failed'
    try:
        return alternative_details.insert_one({
            "product_name" : product_name,
            "product_code" : int(bar_code),
            "product_details" : details,
            "userID" : userID
        })
    except Exception as e:
        print(str(e))
        return "Could not add to perplexity"

async def add_product_to_perplexity_db_uuid(product_name, bar_code, details, userID):
    try:
        check_product_exists = alternative_details_uuid.find_one({'product_code': bar_code, "userID": userID})
        if check_product_exists:
            return alternative_details_uuid.find_one_and_update({'product_code': bar_code, "userID": userID}, {"$set" : {"product_details" : details}})
    except Exception as e:
        print(e)
        return 'Database query failed'
    try:
        return alternative_details_uuid.insert_one({
            "product_name" : product_name,
            "product_code" : bar_code,
            "product_details" : details,
            "userID" : userID
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
        content_settings = ContentSettings(
            content_type="image/png",  # Set the content type, e.g., 'application/pdf'
            content_disposition="inline"  # 'inline' allows viewing in the browser without download
        )
        blob.upload_blob(img, overwrite = True, content_settings = content_settings)
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

async def find_products_with_non_empty_imgfield():
    try:
        products = productsClient.aggregate([
            {
                "$match": {
                    "img_url": { "$ne": "", "$ne": None },
                    "product_name": { 
                        "$not": { "$regex": "coca cola|fanta", "$options": "i" }  # Exclude 'coca cola' and 'fanta'
                    }
                }
            },
            {
                "$group": {
                    "_id": "$product_name",  # Group by product_name
                    "product_code": { "$first": "$product_code" },
                    "product_details": { "$first": "$product_details" },
                    "img_url": { "$first": "$img_url" },
                    "original_id": { "$first": "$_id" }
                }
            },
            {
                "$project": {
                    "product_name": "$_id",  # Restore product_name
                    "product_barcode": "$product_code",
                    # Extract the first few sentences from product_details for product_summary
                    "product_summary": "$product_details",
                    "image_url": "$img_url",
                    "_id": { "$toString": "$original_id" }  # Convert original _id to string
                }
            }
        ])
        return list(p for p in products)
    except Exception as e:
        print(f"An error occurred: {e}")

async def find_products_by_barcodes(barcodes: list):
    try:
        #products = productsClient.find({"product_code": {"$in": barcodes}})
        products = productsClient.aggregate([
                    {
                        "$match": {
                            "product_code": {"$in": barcodes}
                        }
                    },
                    {
                        "$project": {
                            "_id": {
                                "$toString": "$_id"
                            },
                            "product_barcode": "$product_code",
                            "product_name": 1,
                            # Extract the first few sentences from product_details for product_summary
                            "product_summary": "$product_details",
                            "image_url": "$img_url"
                        }
                    }
                ])
        return list(p for p in products)
    except Exception as e:
        print(e)
        return "Error with DB"