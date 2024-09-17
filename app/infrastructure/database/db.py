import pymongo
from config import DATABASE_URI

## Initialize MongoDB client and databases
DBClient = pymongo.MongoClient(DATABASE_URI)
dbClient = DBClient["getAIDB"]
usersClient = dbClient["users"]
productsClient = dbClient["products"]
usersHistoryClient = dbClient["user_history"]
userFeedbackClient = dbClient["user_feedback"]
noProductClient = dbClient["product_not_found"]
alternative_details = dbClient["details_sourced_from_alternatives"]
alternative_details_uuid = dbClient["details_sourced_from_alternatives_uuid"]