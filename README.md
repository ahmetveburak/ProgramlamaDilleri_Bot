# Programlama Dilleri Telegram Botu

Telegram'da birçok yazılım grubunda tekrar tekrar paylaşılan kaynakları ve dahasını
bir araya toplayarak kaynakların daha ulaşılabilir olmasin icin gelistirilmistir.
[Programlama Dilleri](https://t.me/programlama_bot)
  
## Hakkinda
API baglantisi eklendikten sonra proje dogrudan calismamaktadir.
[Programlama Dilleri API](https://github.com/ahmetveburak/ProgramlamaDilleri_API)
projesi kullanilarak calistirilabilir. Botun test edilmesi ve kullanilabilmesi icin
hazir kaynak verisi de eklenmistir fakat ayri bir sekilde calistirmak icin yeterli degildir.
Projenin paylasim amaci kopya bir kaynak botu olusturulmasi yerine 
kendimce uyguladigim menu/navigasyon yapisini best practice olmasa da oneri olarak
paylasmaktir :)
  
Her ne kadar durumdan hosnut olmasam da bot icerisinde ucretli kaynaklar da paylasilmaktadir.
Bu kaynaklar arasinda Turkce icerik var ise bildirmeniz yeterlidir fakat su an 1 USD = 10 TL
oldugu durumda yabanci iceriklerin tolere edilebilecegini dusunuyorum (onerilere acigim).
  
Gerekli bagimliliklar ve API kurulduktan sonra bot calistirilmadan once API calistirilmalidir.
`prodil.ini` dosyasinda gerekli konfigurasyon bilgileri doldurulup bot kullanilabilir.
```shell
python -m prodil
```

## Guncellemeler
_(Ilk yaptigim vasat(:D) adimlari hatirlamiyorum fakat son eklemeleri belirtmek iyi olabilir.)_

### _Kasim 2021_
- Bot dogrudan bir veritabani kullanmak yerine kaynak yonetimini daha pratik
bir sekilde yapabilmek icin Django REST API ile entegre bir sekilde calisir hale getirildi.
- Butun kaynaklar tek seferde listelenmek yerine sayfalara ayirildi.
- Indirilmek istenen kaynaklar sira numarasi yerine buton ile secilir hale getirildi.

### ???? 2020
- Kaynaklari yonetebilmek icin Django entegre edildi.

Proje her turlu gorus ve oneriye acik olup bu yazdiklarimin muhtemelen okunmayacagi dusunulmektedir :D 