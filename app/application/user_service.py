import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..schema_templates.otp_template import html_content
from ..infrastructure.database.db import userFeedbackClient, usersClient, usersHistoryClient
from ..schema_templates.templates import SignUp, LogIN, UpdateProfile, language_code
from bson.objectid import ObjectId

async def check_user_exists(email: str):
    try:
        user = usersClient.find_one({"email": email})
        return user
    except Exception as e:
        print(e)
        return "user not found"

async def create_user(payload: SignUp):
    try:
        result = usersClient.insert_one(dict(payload))
        return "success", result
    except Exception as e:
        print(e)
        return "Error with user creation"

async def create_user_history(user_id: str):
    try:
        usersHistoryClient.insert_one({
            "uid": user_id,
            "product_history": [],
            "chat_history": {}
        })
    except Exception as e:
        print(e)
        return  "Error with user history creation"

async def find_user_by_email(email: str):
    try:
        user = usersClient.find_one({"email": email})
        return user
    except Exception as e:
        print(e)
        return "Error with DB while finding user by email"
    
async def find_user_by_id(userID):
    try:
        user = usersClient.find_one({"_id":ObjectId(userID)})
        return user
    except Exception as e:
        return "Error with DB while finding user by ID"


async def find_user_by_phone(phone_no: str):
    try:
        user = usersClient.find_one({"phone_no": phone_no})
        return user
    except Exception as e:
        print(e)
        return "Error with DB while finding user by phone"

async def validate_user(details: dict, password: str):
    if details and details["password"] == password:
        return {
            "message": "Sign In successful",
            "uid": str(details["_id"]),
            "user_name": details["user_name"],
            "email": details["email"],
            "phone_no": details["phone_no"],
            "country": details["country"],
            "preferred_language": details["preferred_language"]
        }
    elif details:
        return "Wrong password"
    else:
        return "USer not found"


async def add_to_user_product_hist(prod_code, user_id):
    try:
        curr_uh = usersHistoryClient.find_one({"uid" : user_id})
    except Exception as e:
        print(str(e))
        return "error in db for getting user history"
    
    #print(curr_uh)

    try:
        curr_uh["product_history"].append(int(prod_code))
    except Exception as e:
        print(str(e))
        return "Error in adding new product to history"
    #print(curr_uh)

    try:
        usersHistoryClient.find_one_and_update({"uid" : user_id}, {"$set": curr_uh})
        return "success", "added"
    except Exception as e:
        print(str(e))
        return e

async def add_to_user_chat_hist(conv, user_id, prod_id):
    try:
        curr_uh = usersHistoryClient.find_one({"uid" : user_id})
    except Exception as e:
        return str(e)
    
    if prod_id in curr_uh["chat_history"].keys():
        curr_uh["chat_history"][prod_id].append(conv)
    else:
        curr_uh["chat_history"][prod_id] = [conv]

    try:
        usersHistoryClient.find_one_and_update({"uid" : user_id}, {"$set" : curr_uh})
    except Exception as e:
        return str(e)
    
    return "Success", "Added"

async def send_otp_mail(email, password, otp, html_content = html_content):
    # Email details
    sender_email = "getaicompany@gmail.com"
    receiver_email = email
    password = password
    subject = "Your OTP for signup"
    html_content = html_content.replace("{{ otp }}", otp)
    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))
    
    # Connect to the Gmail SMTP server using SSL
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print("Email sent successfully!")


async def get_user_history(ID: str):
    try:
        u_h = usersHistoryClient.find_one({"uid": ID})
    except:
        return "Error in DB"
    
    if u_h:
        return {'product_history': u_h["product_history"]}
    else:
        return "User history not found"

async def get_user_chat_history(userID: str, barcode: str):
    try:
        u_h = usersHistoryClient.find_one({"uid": userID})
    except:
        return "Error with DB"
    
    if u_h:
        if barcode in u_h["chat_history"]:

            return  {"chat_history" : u_h["chat_history"][barcode]}
        else:
            return {
                "chat_history" : []
            }
    else:
        return "User history not found"
    
async def update_user_details(user_id, update_data):
    try:
        updated_result = usersClient.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=True  # Returns the updated document if needed
        )
        if not updated_result:
            return "Error updating user details"
        return {"message": "User details updated successfully"}
    except Exception as e:
        print(e)
        return "Error updating user details"

async def give_user_feedback(userID:str, feedback:str, product_name:str = None):
    try:
        userFeedbackClient.insert_one({"uid" : userID,
                                       "product_name": product_name,
                                       "feedback" : feedback})
    except:
        return "Error with db in adding feedback"
    
    return {
        "response" : "feedback succesfully added"
    }
