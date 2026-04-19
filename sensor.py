import json
import random
import time
from datetime import datetime
import boto3
import os 
from dotenv import load_dotenv
load_dotenv()
# --- YAPILANDIRMA ---
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_SECRET_KEY")
REGION = os.getenv("AWS_REGION")
STREAM_NAME = os.getenv("KINESIS_STREAM_NAME")

# --- AWS CLIENT BAĞLANTISI ---
kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

def generate_traffic_data():
    """Kavşak bazlı trafik yoğunluk verisi üretir."""
    vehicle_count = random.randint(0, 150)
    avg_speed = round(random.uniform(10.0, 90.0), 2)
    occupancy_rate = round((vehicle_count / 150) * 100, 2)
    
    data = {
        "junction_id": "ANKARA_KIZILAY_04",
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "vehicle_count": vehicle_count,
            "average_speed_kmh": avg_speed,
            "occupancy_percentage": occupancy_rate
        },
        "road_status": "CONGESTED" if occupancy_rate > 80 else "FLOWING"
    }
    return data

if __name__ == "__main__":
    print(f"--- {STREAM_NAME} Simülasyonu Başlatıldı ---")
    while True:
        try:
            # 1. Veriyi Üret
            traffic_data = generate_traffic_data()
            
            # 2. JSON Formatına Çevir
            payload = json.dumps(traffic_data)
            
            # 3. Kinesis'e Gönder
            response = kinesis_client.put_record(
                StreamName=STREAM_NAME,
                Data=payload,
                PartitionKey=traffic_data["junction_id"]
            )
            
            print(f"Veri Gönderildi: {traffic_data['road_status']} | Seq: {response['SequenceNumber'][:20]}...")
            
        except Exception as e:
            print(f"HATA OLUŞTU: {e}")
            
        # 4. 1 Saniye Bekle
        time.sleep(1)