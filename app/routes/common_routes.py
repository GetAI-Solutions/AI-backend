from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from io import BytesIO
from PIL import Image
from ..interface import common_controller
from ..schema_templates.templates import chatTemp


router = APIRouter()

## Define endpoint for uploading a barcode image
@router.post(f"/upload-barcode")
async def upload_barcode(file: UploadFile = File(...)):
    res = await common_controller.upload_barcode(file)
    if len(res) < 2:
        raise HTTPException(status_code=400, detail=res)
    else:
        return res[1]

## Define endpoint chatting
@router.post("/chat")
async def chat_with_model(payload: chatTemp):
    # Step 1: Get product details
    try:
        response = await common_controller.chat_with_model(payload)
    except Exception as e:
        raise HTTPException(400, detail = "Unknown Error in Getting response")
    if type(response) == str:
        raise HTTPException(400, detail = response)
    else:
        if response[0] == "success":
            return response[1]
        else:
            raise HTTPException(400, detail = response)
        
## Define endpoint For getting details from perplexity
@router.post("/get-details-from-perplexity")
async def source_from_perplexity(product_name:str = Form(...), bar_code: str = Form(...)):
    try:
        resp = await common_controller.product_from_perplexity(product_name, bar_code)
    except Exception as e:
        raise HTTPException(400, "Unknown Error")
    
    if type(resp) == str:
        raise HTTPException(400, resp)
    
    return {
        "product_name": product_name,
        "product_code": bar_code,
        "product_details": resp["response"][1]
    }


