from configurations import collection  
from database.models import Training  
import requests  
from bs4 import BeautifulSoup  
from fastapi import HTTPException  
import copy  
from pprint import PrettyPrinter  
import time  

printer = PrettyPrinter()  

def get_training_data():
    url = "https://webservice.infinityyazilim.com/Api/CatalogTrainingNameList?token=D60338DE-881A-466D-998A-F0B11821A73D"  
    try:
        response = requests.get(url)  
        response.raise_for_status()  
        content = response.text  
        soup = BeautifulSoup(content, 'html.parser')  
        container_div = soup.find('div', class_='container body-content')  
        
        if not container_div:  
            return {"error": "Container div not found."}
        
        training_list = []  # Eğitim verilerini saklayacağımız liste 
        divs = container_div.find_all('div')  
        
        if len(divs) < 3:  
            return {"error": "Training data structure is invalid."}
        
        # İlk eğitim verisi 
        previous_training = {
            "title": divs[0].get_text().strip().replace("Eğitim Adı:", "").strip(),
            "category": [kategori.strip() for kategori in divs[1].get_text().strip().replace("Kategori:", "").strip().split(",") if kategori.strip()],
            "description": divs[2].get_text().strip().replace("Açıklama:", "").strip()
        }

        # Sonraki eğitimler 
        for i in range(3, len(divs), 3):  
            if i + 2 >= len(divs):  
                break   
            
            current_training = {
                "title": divs[i].get_text().strip().replace("Eğitim Adı:", "").strip(),
                "description": divs[i+2].get_text().strip().replace("Açıklama:", "").strip()
            }
            
            category_name = divs[i+1].get_text().strip().replace("Kategori:", "").strip()
            
            if current_training["title"] == previous_training["title"]:
                if category_name and category_name not in previous_training["category"]:
                    previous_training["category"].append(category_name)
            else:
                current_training["category"] = [kategori.strip() for kategori in category_name.split(",") if kategori.strip()]
                training_list.append(copy.deepcopy(previous_training))  
                previous_training = {  
                    "title": current_training["title"],
                    "category": current_training["category"],
                    "description": current_training["description"]
                }
        
        training_list.append(copy.deepcopy(previous_training))  
        
        # Veritabanı işlemleri: Yeni eğitimleri ekler ve mevcut olanları günceller 
        inserted_ids = []  
        updated_ids = []  
        
        for training in training_list:
            existing_training = collection.find_one({"title": training["title"]})  
            if existing_training:
                existing_categories = existing_training.get("category", [])  
                if len(existing_categories) == len(training["category"]):  
                    continue  
                else:
                    collection.update_one(
                        {"_id": existing_training["_id"]},
                        {"$set": {"category": training["category"], "description": training["description"]}}
                    )
                    updated_ids.append(str(existing_training["_id"]))  
            else:
                new_training = Training(**training)  
                resp = collection.insert_one(new_training.dict())  
                inserted_ids.append(str(resp.inserted_id))  

        # Sonuçları döndürür: Eklenen ID'ler, güncellenen ID'ler ve eğitimler.
        return {
            "status_code": 200,
            "inserted_ids": inserted_ids,
            "updated_ids": updated_ids,
            "trainings": training_list
        }
    
    except Exception as e: 
        return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# search_service çalıştırma süresi: ~50.0 ms")
# Eğitim başlıklarında arama yapar ve sonuçları döndürür.
def search_service(query: str):
    #start_time = time.time()  # Başlangıç zamanını al
    result = collection.aggregate([  # Veritabanında arama 
        {
            '$search': {
                "index": "training_language_search",  
                "compound": {
                    "must": [
                        {
                            "text": {
                                "query": query,  
                                "path": "title",  # Başlıkta arama 
                                "fuzzy": {},  
                                "score": {"boost": {"value": 4.0}}  # Başlıklara daha fazla puan 
                            }
                        },
                    ],
                    "should": [
                        {
                            "text": {
                                "query": query,  # Kategoriye göre arama 
                                "path": "category",
                                "fuzzy": {},
                                "score": {"boost": {"value": 3.0}}  # Kategorilere daha düşük puan 
                            }
                        },
                        {
                            "text": {
                                "query": query,  # Açıklama kısmına göre arama 
                                "path": "description",
                                "fuzzy": {},
                                "score": {"boost": {"value": 2.0}}  # Açıklamalara daha da düşük puan 
                            }
                        }
                    ]
                }
            }
        },
        {
            "$project": {
                "_id": 0,  
                "title": 1  # Yalnızca başlıklar 
            }
        },
        {
            '$limit': 10  # En fazla 10 sonuç 
        }
    ])
    #execution_time = (time.time() - start_time) * 1000  # Milisaniyeye çevir
    #print(f"search_service çalıştırma süresi: {execution_time:.2f} ms")
    #printer.pprint(list(result))  # Arama sonucunu yazdır 
    return list(result)  