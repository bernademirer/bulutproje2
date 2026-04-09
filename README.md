# 3522 Bulut Bilişim Dersi - Proje 2
## Gerçek Zamanlı Veri Akışı ve İşleme (IoT Simülasyonu)


### 1. Proje Amacı ve Kapsamı
Bu projede, bir IoT cihazından gelen verilerin (trafik yoğunluğu) MQTT/WebSocket protokolleri kullanılarak AWS bulut platformuna aktarılması ve gerçek zamanlı analiz edilmesi hedeflenmektedir.

### 2. Kullanılan Teknolojiler
**Dil:** Python 
**Bulut:** AWS (Kinesis, Lambda, DynamoDB)
**Protokol:** MQTT / Boto3 SDK 

### 3. Günlük Çalışma Raporu (Log)
**Tarih: 09.04.2026**
*Proje reposu oluşturuldu ve README dosyası hazırlandı.
* Python ortamı yapılandırıldı boto3 kütüphanesi kuruldu.
* AWS hesap aktivasyon süreci başlatıldı (Onay bekleniyor). Kinesis'e bağlanmaya çalıştığımda "Complete your account setup" başlığı altında bir sayfaya yönlendirdi ve "It might take up to 24 hours to fully activate your AWS services." şeklinde bir uyarı verdi.
* Veri simülasyonu için `sensor.py` iskeleti oluşturuldu.
*MQTT Entegrasyonu yapıldı.  Projenin IoT standartlarına uygun olması için `paho-mqtt` kütüphanesi sisteme dahil edildi.