from flask import Flask, render_template, request, jsonify  
from services import search_service, get_training_data  

app = Flask(__name__)  

# Rendering
@app.route("/")
def main():
    return render_template("index.html")  

# Kullanıcı mesajını işler 
@app.route("/get")
def get_chatbot_response():
    userText = request.args.get('userMessage')  
    search_results = search_service(userText)  
    if search_results:
        titles = [result["title"] for result in search_results]  
        return jsonify(titles)  
    return jsonify(["Aradığınız konuyla ilgili eğitim bulunamadı."])  

# Eğitim verisi oluşturmak için POST isteği alır
@app.route("/create_from_url", methods=["POST"])
def create_training_from_url():
    return jsonify(get_training_data())  

# Eğitim araması yapar 
@app.route("/search", methods=["GET"])
def search_training():
    query = request.args.get("query") 
    return jsonify(search_service(query))  

if __name__ == "__main__":
    app.run(debug=True)