import numpy as np
from PIL import Image
import numpy as np
import cv2
from pyzbar import pyzbar

async def scan_barcode_from_image(image):
    image_np = np.array(image.convert('RGB'))
    barcodes = pyzbar.decode(image_np)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        text = f'{barcode_data} ({barcode_type})'
        cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image_np, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return Image.fromarray(image_np), barcodes