from config import contClient, load_blob
from azure.storage.blob import ContentSettings
from app.infrastructure.database.db import productsClient, noProductClient, alternative_details, alternative_details_uuid

allnoImg = productsClient.aggregate([
    {
        "$match": {
            "img_url": { "$ne": "", "$ne": None }
        }
    },
    {
        "$project": {
            "product_code": 1,
            "_id": 0
        }
    }
])

all_b = [p['product_code'] for p in list(allnoImg)]

for b in all_b:
    print(str(b) + ".png")
    blob = load_blob(contClient, str(int(b)).lstrip('0') + ".png")
    content_settings = ContentSettings(
            content_type="image/png",  # Set the content type, e.g., 'application/pdf'
            content_disposition="inline"  # 'inline' allows viewing in the browser without download
        )
    try:
        blob.set_http_headers(content_settings=content_settings)
        with open("urls.txt", "a") as f:
            f.write(blob.url + "\n")
        print(b, blob.url)
    except Exception as e:
        print(b)
