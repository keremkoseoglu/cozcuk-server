# Çözcük

Çözcük, basit bir şifre çözme oyunudur - kurallarını /help.html dosyasında görebilirsiniz. Bu projenin amacı; modern 
bir uygulamada olması gereken bazı özellikleri basit bir yapı bünyesinde ortaya koymaktır. Kodlama, Python ile
yazılmış ve Flask Web Framework kullanılmıştır.

## Özellikler

Proje kapsamında, aşağıdaki özellikler uygulanmıştır:
- Veritabanı erişimi (Postgre)
- Abstract Class sayesinde alternatif veritabanları ile çalışabilme (Data Access Object Design Pattern)
- Login, Session
- Hatalı girişte Captcha talebi
- "Şifremi unuttum"
- E-Posta gönderimi (Mailgun üzerinden)
- Abstract Class sayesinde alternatif E-Posta servis sağlayıcıları ile çalışabilme
- Facebook üzerinden OAuth
- REST / JSON tabanlı servisler
- Bu servislere erişen JQuery kodları (AJAX)
- Kullanıcı / Admin sayfası ayrımı
- Git entegrasyonu

## Proje Yapısı

### /

Burada, uygulamanın ana dosyaları yer almaktadır. 
- **app.py**: Flask'in öngördüğü ana site dosyası
- **Procfile**: Site Heroku'da Host edildiği zaman gereken başlangıç dosyası
- **requirements.txt**: pip freeze ile oluşturulmuş kütüphane dosyası

### /cozdata

Veritabanı haberleşmesi ile ilgili dosyalar, burada yer almaktadır. 
- **dao.py**: Veritabanları için Abstract Class. Her veritabanı için, bundan türetilmiş bir dosya + sınıf olmalıdır.
- **hard_code.py**: Veritabanına erişim olmadığı durumda geliştirme yapabilmek için oluşturulmuş farazi veritabanı
- **postgre.py**: Postgre iletişimini sağlar
- **factory.py**: Environment Variable'da belirlenmiş veritabanı için dinamik nesne yaratıp döndürür

Yeni bir veritabanı ile çalışmak isterseniz;
- Yeni veritabanı için postgre.py 'ye benzer şekilde bir dosya oluşturun
- **DATA_CLASS** adlı Environment Variable'ına yeni veritabanı **sınıfınızın** ismini yazın (örnek: HardCode, Postgre)

### /cozmail

Veritabanına benzer mimaride; E-Posta gönderme ile ilgili dosyalar burada yer almaktadır.
- **mao.py**: E-Posta hizmet sağlayıcıları için Abstract Class. Her bir hizmet sağlayıcı için, bundan türetilmiş bir dosya + sınıf olmalıdır.
- **mailgun.py**: Mailgun üzerinden E-Posta göndermek için sınıf. Bu sınıftaki kodlar, Mailgun'un öngördüğü Environment Variable'ları kullanmaktadır. 
- **factory**: Enviroment Variable'da berlirlenmiş E-Posta servis sağlayıcısı için dinamik nesne yaratıp döndürür.

Yeni bir servis sağlayıcı ile çalışmak isterseniz;
- Yeni servis sağlayıcı için **mailgun.py** 'ye benzer şekilde bir dosya oluşturun.
- **MAIL_CLASS** adlı Environment Variable'ına yeni E-Posta **sınıfınızın** ismini yazın (örnek: Mailgun)

### /cozmodel

Bu pakette; model sınıflar bulunmaktadır. 
- **puzzle.py**: Bilmece
- **user.py**: Kullanıcı

Bu sınıfların; veritabanı, E-Posta gibi sınıflara doğrudan erişmediğine dikkat edin. Bu kavramlar Decoupled bir halde
tanımlanmış, bu şekilde mimari esneklik yükseltilmiş ve değişiklik durumundaki modifikasyon ihtiyacı azaltılmıştır.

### /cozweb

Bu pakette, doğrudan Web ile ilişkili yardımcı işlevler bulunmaktadır.
- **captcha.py**: Hatalı şifre girildiğinde, karşımızda bir insan olduğundan emin olmak için gösterdiğimiz Captcha görsellerini üretir. 
- **http.py**: App, Session gibi nesneler ile ilgili yardımcı işlevler barındırır.

Captcha görselleri, static/captcha klasöründe saklanır. Herhangi bir Admin Login olduğunda, eski Captcha görselleri bu klasörden temizlenir.

### /static

Flask'in öngördüğü sabit içerik klasörüdür. 

### /templates

Flask'in öngördüğü şablon içerik klasörüdür.

## Yardımcı Projeler

Eş anlamlı kelimelerden otomatik bilmece üreten [Çözcük Generator](https://github.com/keremkoseoglu/cozcuk-generator) programı geliştirilmiştir.