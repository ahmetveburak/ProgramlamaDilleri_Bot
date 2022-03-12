class BotMessage:
    WELCOME = (
        "__Hoşgeldin__ "
        "**%(first_name)s** "
        "__botun kullanımı sırasında bir sorunla karşılaşırsan tekrardan__ "
        "/start __komutunu çalıştırabilirsin. Önerebileceğin kaynaklar "
        "veya geri bildirimlerin icin__ /hakkinda "
        "__kısmından bize ulaşabilirsin.__"
    )
    NO_RESOURCE = "Bu alanda henuz kaynak bulunmamaktadir."
    ERROR_RESOURCE = (
        "%(doc_names)s\n\n" "Isimli dosyalar gonderilirken sorun olustu. " "Geri bildirim icin: @musaitbiyerde"
    )
    RESTART = "Tekrar baslamak istersen /start komutunu calistirabilirsin."
    NO_CHOICE = "Herhangi bir kaynak secilmedi!"


SELECTED = "🟢"
NOT_SELECTED = "🔴"
