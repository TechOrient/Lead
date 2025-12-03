# FirmaAI- Open Firma Card

Bu proje, Llama,Openai(GPT-4o-search-preview) modellerinin altyapısını kullanarak bir mail adresinden/ mail imzasından bir şirketin gerekli bilgilerini (şirket adı, kısa ad,adres, şehir,ülke,vergi numarası vb.) search-preview ile araştırma yaparak kayıt ederek kullanılan ERP sisteminde bir firma kartı açmayı sağlayan orta-büyük ölçekli bir projedir. 
Proje  iki ana aşamadan oluşmaktadır: 

## Ana Başlıklar
- Mail adresi alınması 
- Mail imzasının analizi 
- Alınan bilgiler üzerinden arama yapılması
- Alınan bilgilerin kaydı 
- ERP sistemine API ile entegrasyon 
- Bilgilerin ERP'de firma kartı olarak açılması


### 1. Mail adresi üzerinden ya da mail imzasından bilgilerin alınması 

Projenin ilk etabı olan şirket bilgilerinin çekilmesi. Bu etapta AI altyapısı kullanılarak şirkete ait bilgiler AI üzerinden aranarak gerekli bilgilere ulaşım sağlanıyor. Yakalanan bu bilgiler bir database .json formatında kayıt ediliyor. 

### 2. Kayıt edilen bilgilerin API üstünen gönderimi 

Bu etapta ise kayıt edilen bilgilerin gerekli alanlara gönderimi yapılmaktadır. Geliştirilen API bağlantısı sayesinde gönderilecek olan bilgiler ERP sistemine gönderimi yapılıyor.




## Kullanım 
- AI Modelleri : OpenAI(4o+search_preview) : Bilgilerin internette aranması / Llama  : Mail imzasından gerekli bilgilerin çekilmesi
- Maillere erişim : Microsoft GRAPH API : Maillere erişim ve de gerekli maillerin tespit edilmesini sağlama
- Database : MongoDB kullanılıyor. Sebebi ise hızlı, kolay, analiz hızlı, verilerin json formatında tutulması gibi birçok sebep var 
- API : Kullanılan ERP sistemine erişimi ve de gerekli firma kartlarını açmak için kullanımı 


## Dosyalar ve Açıklamaları

### 1. `main.py`
Ana kodun çalıştığı dosya. Bu dosya, şirket bilgilerini arama, özetleme ve rapor oluşturma işlemlerini bir akış grafiği (StateGraph) kullanarak gerçekleştirir.


### 2. `api_entegration.py`
ERP sistemine veri göndermek için kullanılan API entegrasyon modülü. Bu modül, bir token alır ve gerekli bilgileri API'ye gönderir.





## Güvenlik

- Konfigürasyon dosyaları (.cfg, .env) GitHub'a yüklenmemelidir.
- Client secret gibi hassas bilgileri paylaşmayın.
- Token'lar otomatik olarak önbelleklenir ve güvenli şekilde yönetilir.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
