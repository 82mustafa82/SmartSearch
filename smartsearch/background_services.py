from apscheduler.schedulers.background import BackgroundScheduler
import time  
from services import get_training_data  

# Arka planda çalışacak zamanlayıcı
scheduler = BackgroundScheduler()

# Her gün gece yarısı (00:00) çalışacak 
scheduler.add_job(get_training_data, 'cron', hour=0, minute=0)  

scheduler.start()

# Bu döngü programın sürekli çalışmasını sağlar.
while True:
    time.sleep(1)  # CPU kullanımını azaltma