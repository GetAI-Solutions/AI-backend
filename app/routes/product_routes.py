from fastapi import APIRouter, Form, HTTPException, UploadFile, File
from ..interface import product_controller
from typing import Literal

router = APIRouter()

@router.post("/get-product")
async def get_product(bar_code: str = Form(...)):
    product = await product_controller.find_product_by_barcode(bar_code)
    if len(product) > 1:
        product = product[1]
        return {
            "_id": str(product["_id"]),
            "product_code": product["product_code"],
            "product_name": product["product_name"],
            "product_details": product["product_details"]
        }
    else:
        raise HTTPException(status_code=404, detail="Error getting product")
    
## Define endpoint for retrieving product summary
@router.post(f"/get-product-summary")
async def get_product_summary(bar_code: str = Form(...), userID: str = Form(...)):
    try:
        resp = await product_controller.get_product_summary(bar_code, userID)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=404, detail="Error in getting summary")
    if type(resp) == str:
        raise HTTPException(status_code=404, detail=resp)
    else:
        if resp[0] == "success":
            return resp[1]
        else:
            HTTPException(status_code=404, detail=str(resp))

## Define endpoint for retrieving product summary
@router.post(f"/add-product-to-db")
async def add_product_to_db(file: UploadFile, product_code: str, product_name: str):
    try:
        resp = await product_controller.add_product_to_db(file, product_code, product_name)
    except:
        raise HTTPException(status_code=404, detail="Unknown Error")
    
    if type(resp) == str:
        raise HTTPException(status_code=404, detail=resp)
    else:
        return resp

@router.get(f"/get-all-products")
async def get_all_products(option : Literal["InDB", "notInDB", "perplexity", "NoIMG"]):
    try:
        all_products = await product_controller.get_all_products(option)
    except:
        raise HTTPException(status_code=400, detail="Unknown Error")
    
    if type(all_products) == str:
        raise HTTPException(status_code=400, detail=all_products)
    
    return all_products

@router.post(f"/add-picture-to-product")
async def add_img_to_product(file: UploadFile = File(...), bar_code: str = Form(...)):
    try:
        resp = await product_controller.add_img_to_product(file, bar_code)
    except Exception as e:
        raise HTTPException(status_code=400, detail= "Unknown Error" + str(e))
    if type(resp) == str:
        raise HTTPException(status_code=400, detail= resp)
    
    return resp

@router.post(f"/search-products-by-name")
async def search_product_by_name(product_name: str = Form(...)):
    try:
        product = await product_controller.get_products_by_name(product_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Unknown Error")
    
    if type(product) == str:
        raise HTTPException(status_code=404, detail=product)
    
    return product

@router.get(f"/get-home-page-products")
async def get_home_page_products():
    try:
        products = await product_controller.get_home_page_products()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Unknown Error")
    
    if type(products) == str:
        raise HTTPException(status_code=404, detail=products)
    
    return products

@router.post(f"rate-product")
async def rate_product(product_id: str = Form(...), rating: int = Form(...)):
    try:
        resp = await product_controller.rate_product(product_id, rating)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Unknown Error")
    
    if type(resp) == str:
        raise HTTPException(status_code=404, detail=resp)
    
    return resp[1]