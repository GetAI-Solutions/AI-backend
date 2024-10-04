from dotenv import load_dotenv
import os
from azure.storage.blob import BlobServiceClient, ContentSettings
from openai import OpenAI
import requests
import json

load_dotenv()
appENV = os.getenv("APP_ENV", "local")
OAI_KEY = os.getenv("OAI_KEY", "local")
DATABASE_URI = os.getenv("DATABASE_URI", "local")
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")
g_app_password = os.getenv("G_APP_PASSWORD")
OAI_KEY_TOKEN = os.getenv("OAI_KEY_TOKEN", "local")
blob_conn_str = os.getenv("BLOLB_CONNECTION_STRING")
Perplexity_KEY = os.getenv("PERPLEXAI_KEY")
CONT_NAME = os.getenv("CONT_NAME")
GCLOUD_JSON_URL = os.getenv("GCLOUD_JSON_URL")

def load_cont(container_name, blob_conn_str):
    blob_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
    container_client = blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        container_client = container_client.create_container()
        container_client = blob_service_client.get_container_client(container_name)
    return container_client

def load_blob(container_client, blob_name):
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client

contClient = load_cont(CONT_NAME, blob_conn_str)

bot = OpenAI(
    api_key=OAI_KEY
)

# Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key.
try:
    with open("gcloud_cred.json", "w") as f:
        json_f = requests.get(GCLOUD_JSON_URL).json()
        json.dump(json_f, f)
except Exception as e:
    print("Unable to download Gcloud cred for TTS \n"+str(e))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcloud_cred.json"