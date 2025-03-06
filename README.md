# 📌 SmartSearch Eğitim Öneri Chatbot

![GitHub](https://github.com/82mustafa82/SmartSearch)

Bu proje, Flask tabanlı bir web uygulamasıdır ve kullanıcıların belirli bir konu veya yetkinlik için eğitim önerileri almasını sağlar. Eğitim verileri MongoDB'de saklanır ve chatbot, kullanıcıdan gelen sorgulara göre ilgili eğitimleri döndürür.

## 🚀 Başlangıç

Aşağıdaki adımları takip ederek projeyi yerel ortamınızda çalıştırabilirsiniz.

### ⚙️ Gereksinimler

- Python 3.12
- Flask
- MongoDB
- virtualenv (Opsiyonel)
- APScheduler==3.11.0
- beautifulsoup4==4.13.3
- certifi==2025.1.31
- fastapi==0.115.8
- Flask==3.1.0
- pydantic==2.10.6
- pydantic_core==2.27.2
- pymongo==4.11.1
- requests==2.32.3
- typing_extensions==4.12.2

### ⚙️ Özellikler

- Flask kullanılarak geliştirildi.
- MongoDB ile eğitim verilerini yönetir.
- jQuery kullanılarak dinamik bir kullanıcı arayüzü sağlar.
- Arama işlemi için MongoDB'nin $search özelliği kullanılır.
- Eğitim verileri belirli aralıklarla web scraping yöntemiyle güncellenir.

### 📥 Kurulum

1. **Sanal ortam oluşturun**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Gerekli Bağımlılıkları Yükleyin**
   ```
   cd smartsearch
   pip install -r requirements.txt
   ```

3. **MongoDB Bağlantısını Güncelleyin**
	configurations.py dosyasında bulunan MongoDB bağlantı URI'sini kendi veritabanınıza göre güncelleyin:
   ```
   uri = "mongodb+srv://<username>:<password>@<cluster-url>/"
   ```

4. **Uygulamayı Çalıştırın**
	Flask uygulamasını başlatmak için aşağıdaki komutu çalıştırın:
   ```
   python index.py
   ```
   Arka planda çalışan eğitim verisi güncelleme hizmetini başlatmak için:
   ```
   python background_services.py
   ```

## 🔗 API Kullanımı

1. **Ana Sayfa**
Tarayıcınızda aşağıdaki URL'yi açarak chatbot arayüzüne ulaşabilirsiniz:
```
http://127.0.0.1:5000/
   ```

2. **API Endpoint'leri**

| Endpoint                 | Yöntem | Açıklama |
|--------------------------|--------|----------|
| `/get`  				   | GET    | Kullanıcının gönderdiği mesajı alır ve ilgili eğitimleri döndürür.  |
| `/create_from_url`       | POST   | Eğitim verilerini belirli bir URL'den çeker ve MongoDB'ye kaydeder. |
| `/search?query=<kelime>` | GET    | Belirtilen kelimeye göre eğitimleri arar ve sonuçları döndürür.  	  |

## 📞 İletişim

Eğer herhangi bir sorunuz varsa, benimle iletişime geçmekten çekinmeyin!
- GitHub: [@82mustafa82](https://github.com/82mustafa82)
- E-posta: 82mustafa82@gmail.com
