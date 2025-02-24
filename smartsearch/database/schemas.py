# Her bir eğitim verisini belirli bir yapıya dönüştürür.
def individual_data(training):
    return {
        "id": str(training["_id"]),  
        "title": training["title"],  
        "category": ", ".join(training["category"]),  
        "description": training["description"]  
    }

# Tüm eğitim verilerini işleyip bir liste döndürür.
def all_trainings(trainings):
    return [individual_data(training) for training in trainings]  