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

### Gün 1 (Devam) - 09.04.2026: AWS Entegrasyonu ve Canlı Akış

* **AWS Servis Aktivasyonu:** Hesap yükseltme (upgrade) işlemleri tamamlanarak servisler tam yetkiyle kullanıma açıldı.
* **Kinesis Yapılandırması:** AWS üzerinde **On-demand** kapasite modunda `BulutProjeStream` adlı veri akış kanalı (stream) oluşturuldu.
* **Canlı Veri Akışı:** `sensor.py` scripti üzerinden üretilen trafik verileri, Boto3 SDK kullanılarak AWS Kinesis platformuna saniyede 1 paket olacak şekilde gönderilmeye başlandı.
* **Veritabanı Hazırlığı:** Gelen verilerin kalıcı olarak saklanması amacıyla DynamoDB üzerinde `TrafikVerileri` tablosu; `junction_id` (Partition Key) ve `timestamp` (Sort Key) yapısıyla oluşturuldu.

---

###  Karşılaşılan Teknik Sorunlar ve Çözümler

 **UnrecognizedClientException**  AWS sisteminin gönderilen güvenlik anahtarlarını (Access Key/Secret Key) tanıyamaması. | IAM üzerinden yeni bir anahtar seti oluşturuldu; tırnak işaretleri ve boşluk karakterleri kontrol edilerek kod içerisinde güncellendi. 
 **AccessDeniedException**  IAM kullanıcısının Kinesis üzerinde `PutRecord` yetkisinin bulunmaması. | AWS IAM paneli üzerinden kullanıcıya `AmazonKinesisFullAccess` politikası atanarak yetkilendirme sağlandı. |
 **Terminal Komut Hatası (cpy)**  VS Code üzerindeki yanlış konfigürasyon nedeniyle komutun `cpy` olarak tetiklenmesi. | VS Code `Executor Map` ayarları düzenlendi ve komut standart `py` launcher'a çekildi. 
 **Metrik Gecikmesi** | CloudWatch grafiklerinin anlık olarak güncellenmemesi.  Veri iletiminin doğrulanması için Kinesis **"Data Viewer"** aracı kullanılarak ham veri (raw data) seviyesinde kontrol yapıldı. 

###  Mevcut Durum 
Şu an projenin **"Veri Üretim"** ve **"Veri Ingestion (Toplama)"** katmanları %100 çalışır durumdadır.
* **Terminal Çıktısı:** Veriler her saniye terminalde analiz edilerek başarıyla AWS'ye iletilmektedir.
* **AWS Doğrulaması:** Kinesis üzerindeki Shard'lar taranmış ve JSON paketlerinin bulut ortamına kayıpsız ulaştığı teyit edilmiştir.
* **Gelecek Adım:** AWS Lambda fonksiyonu yazılarak, Kinesis'e düşen her verinin otomatik olarak DynamoDB tablosuna kaydedilmesi sağlanacaktır.

### Gün 2 19.04.2026

### Tamamlanan Adım: AWS Lambda & DynamoDB Entegrasyonu

Projenin veri işleme (Processing) ve kalıcılık (Persistence) katmanları başarıyla devreye alınmıştır.

#### **1. AWS Lambda: Veri İşleyici (Transformer)**
Kinesis Data Streams üzerinden gelen ham trafik verilerini anlık olarak işlemek üzere bir Python 3.12 Lambda fonksiyonu (`TrafikVeriIsleyici`) yayına alınmıştır.
* **Tetikleme Mekanizması:** 'Event Source Mapping' kullanılarak Kinesis Stream ile Lambda arasında köprü kurulmuştur.
* **Veri Kurtarma (Trim Horizon):** Tetikleyici ayarlarında `Starting Position: Trim Horizon` seçilerek, akış başladığı andan itibaren biriken tüm verilerin kayıpsız işlenmesi sağlanmıştır.

#### **2. Karşılaşılan Teknik Zorluklar ve Çözümleri**
Sistem kurulumu sırasında karşılaşılan problemler ve uygulanan çözümler:
* **IAM Permission Refinement:** Lambda'nın On-demand modundaki Kinesis shard'larını keşfedebilmesi için standart izinlere ek olarak `kinesis:ListShards` ve `kinesis:DescribeStreamSummary` yetkileri 'Inline Policy' olarak tanımlanmıştır.
* **UI Synchronization:** AWS Konsolu üzerindeki görsel 'Grey/Inactive' durum hatasına rağmen, CloudWatch metrikleri üzerinden sistemin fonksiyonelliği (Invocations) doğrulanmıştır.
***Lambda CloudWatch loglarında `Runtime.UserCodeSyntaxError` saptanmıştır.


#### **3. Performans ve Doğrulama**
* **CloudWatch Metrikleri:** Yapılan testlerde Lambda fonksiyonunun **72 kez** başarılı bir şekilde tetiklendiği ve çalışma süresinin (Duration) optimize edildiği gözlemlenmiştir.
* **Veri Kalıcılığı:** DynamoDB `Explore Table Items` üzerinden yapılan sorgulamada, yerel simülatörden gönderilen JSON paketlerinin tabloya başarıyla yazıldığı teyit edilmiştir.

---

###  Mevcut Durum (Özet)
1. **Producer:** `sensor.py` üzerinden saniyede 1 paket veri üretimi aktif.
2. **Ingestion:** Kinesis Data Stream 'On-demand' modda veri topluyor.
3. **Processing:** Lambda fonksiyonu tetikleniyor ve veriyi işliyor.
4. **Storage:** DynamoDB tablosu Ankara trafik verilerini saklıyor.

#### **5. Karşılaşılan Teknik Zorluklar ve Uygulanan Mühendislik Çözümleri**
Projenin yayına alınma sürecinde saptanan kritik hatalar ve uygulanan "Best Practice" çözümler aşağıda listelenmiştir:

* **Veri Tipi Uyuşmazlığı (Type Mismatch):** AWS DynamoDB'nin standart Python `float` veri tipini desteklememesi nedeniyle Lambda üzerinde `Decimal` kütüphanesi entegre edilmiştir. `json.loads(parse_float=Decimal)` metodolojisiyle veri kaybı önlenmiş ve yazma operasyonları stabilize edilmiştir.
* **Kimlik Doğrulama (IAM Authentication):** Producer (`sensor.py`) katmanında yaşanan `UnrecognizedClientException` hatası, IAM Access Key rotasyonu ve kimlik bilgileri doğrulaması ile aşılmıştır.
* **Runtime Syntax & Indentation:** Lambda fonksiyonu üzerinde oluşan sözdizimi hataları, Python PEP 8 standartlarına uygun hiyerarşik düzenleme ve 'Cold Start' deployment süreciyle giderilmiştir.
* **Event Source Mapping (ESM):** Kinesis ve Lambda arasındaki tetikleme (Trigger) senkronizasyon kaybı, tetikleyicinin 'Latest Position' parametresiyle yeniden yapılandırılması sonucu çözülmüştür.

#### **6. Sonuç ve Doğrulama (Verification)**
19.04.2026 itibarıyla sistem uçtan uca test edilmiş; CloudWatch metrikleri üzerinden saniyede 1 paket (700+ başarılı tetiklenme) işleme kapasitesine ulaşıldığı ve DynamoDB tablosuna verilerin hatasız işlendiği teyit edilmiştir.

**Sistem Durumu:**  TAMAMLANDI / AKTİF