# Programlama Dilleri Telegram Botu
Telegram'da birçok yazılım grubunda tekrar tekrar paylaşılan kaynakları ve dahasını bir araya toplayarak kaynakları daha ulaşılabilir hale getirmeyi hedeflediğimiz Programlama Dilleri Botu'dur. Bota ulaşmak için -> [Programlama Dilleri](https://t.me/programlama_bot). _Geliştirme aşaması devam etmektedir._

## Projeyi çalıştırmak için yapılması gerekenler

`git clone https://github.com/ahmetveburak/ProgramlamaDilleri.git`

`cd ProgramlamaDilleri`

`python -m venv .venv`

* Poetry Kurulu ise

`poetry install`

`poetry shell`

* Poetry Kurulu değil ise (_İsteğe kağlı kurmak için_ -> [Python Poetry](https://python-poetry.org/docs/#installation))

`source .venv/bin/activate`

`pip install -r requirements.txt`

* Botu çalıştırmak için

`python -m prodil`