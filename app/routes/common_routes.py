from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from io import BytesIO
from PIL import Image
from ..interface import common_controller
from ..schema_templates.templates import chatTemp
from fastapi.responses import StreamingResponse
import io


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
async def source_from_perplexity(product_name:str = Form(...), bar_code: str = Form(...), userID: str = Form(...)):
    try:
        resp = await common_controller.product_from_perplexity(product_name, bar_code,userID)
    except Exception as e:
        print(str(e))
        raise HTTPException(400, "Unknown Error")
    
    if type(resp) == str:
        raise HTTPException(400, resp)
    
    return {"product": 
        {"product_name": product_name,
        "product_code": bar_code,
        "product_details": resp["response"][1]}
    }

@router.post(f"/search-perplexity-by-name")
async def search_perplexity_by_name(product_name: str = Form(...), userID: str = Form(...)):
    try:
        resp = await common_controller.search_perplexity_by_name(product_name,userID)
    except Exception as e:
        print(str(e))
        raise HTTPException(400, "Unknown Error")
    
    if type(resp) == str:
        raise HTTPException(400, resp)
    
    print(resp)
    return {"product": 
        {"product_name": product_name,
        "product_details": resp["response"][1],
        "product_code": resp["uuid_bar_code"]}
    }

@router.get(f"/get-speech-from-text")
async def get_speech_from_text(text: str = Form(...)):
    try:
        resp = await common_controller.convert_text_to_speech(text)
    except Exception as e:
        print(str(e))
        raise HTTPException(400, "Unknown Error")
    
    if type(resp) == str:
        raise HTTPException(400, resp)
    #return resp[1].audio_content
    audio_stream = io.BytesIO(resp[1].audio_content)
    return StreamingResponse(audio_stream, media_type="audio/wav")



