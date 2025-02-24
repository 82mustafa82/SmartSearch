import certifi
from pymongo.mongo_client import MongoClient


uri = "mongodb+srv://aydinmustafa:<password>@musty-coder.cqajf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())

db = client.training_db
collection = db["training_data"]