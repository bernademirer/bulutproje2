# 3522 Bulut Bilişim Dersi - Proje 2
## Gerçek Zamanlı Veri Akışı ve İşleme (IoT Simülasyonu)

## Proje Konusu:Gerçek zamanlı trafik verilerinin AWS bulut platformu üzerinden işlenmesi ve analizi. 

###  Proje Amacı ve Kapsamı
Bu projede, bir IoT cihazından gelen verilerin (trafik yoğunluğu) MQTT/WebSocket protokolleri kullanılarak AWS bulut platformuna aktarılması ve gerçek zamanlı analiz edilmesi hedeflenmektedir.

###  Kullanılan Teknolojiler
**Dil:** Python 
**Bulut:** AWS (Kinesis, Lambda, DynamoDB)
**Protokol:** MQTT / Boto3 SDK 

###  Veri Yapısı ve Analiz Mantığı
Simüle edilen her paket şu analitik verilere sahiptir:
* `vehicle_count`: Kavşaktaki anlık araç sayısı.
* `average_speed_kmh`: Araçların ortalama hızı (km/sa).
* `occupancy_percentage`: Yolun doluluk oranı.
* `road_status`: Doluluk %80'i geçtiğinde otomatik olarak `CONGESTED` (Yoğun) etiketi atanır; aksi halde `FLOWING` (Akıcı) olarak işaretlenir.

### Gün 1 09.04.2026

*Proje reposu oluşturuldu ve README dosyası hazırlandı.
* Python ortamı yapılandırıldı boto3 kütüphanesi kuruldu.
* AWS hesap aktivasyon süreci başlatıldı (Onay bekleniyor). Kinesis'e bağlanmaya çalıştığımda "Complete your account setup" başlığı altında bir sayfaya yönlendirdi ve "It might take up to 24 hours to fully activate your AWS services." şeklinde bir uyarı verdi.
* Veri simülasyonu için `sensor.py` iskeleti oluşturuldu.
*MQTT Entegrasyonu yapıldı.  Projenin IoT standartlarına uygun olması için `paho-mqtt` kütüphanesi sisteme dahil edildi.

**Karşılaşılan Sorunlar ve Çözümler:**
    * *Sorun:* Python/Pip komutlarının terminalde tanınmaması (PATH hatası).
    * *Çözüm:* Windows Ortam Değişkenleri düzenlendi ve VS Code üzerinde "Python Interpreter" manuel olarak seçildi. Komutlar `py` launcher üzerinden çalıştırılarak standart sağlandı.
* **Trafik Simülatörü (Mock Data):** `sensor.py` scripti yazıldı. Ankara Kızılay bölgesini temsil eden gerçek zamanlı trafik verileri (araç sayısı, hız, doluluk oranı) JSON formatında üretildi.

### Mevcut Durum (Ekran Görüntüsü Notu)
Şu an projenin "Veri Üretim" katmanı tamamlanmış ve yerel testleri başarıyla geçmiştir. AWS hesap onayı beklendiği için veriler terminal üzerinden doğrulanmaktadır.