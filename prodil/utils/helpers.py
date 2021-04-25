from prodil.models.model import session, History, UserInfo, User
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import User as PyroUser
from datetime import datetime
from typing import List


class Question:
    def __init__(self) -> None:
        self.p_lang = {
            "ask": "Hangi programlama dili ile ilgileniyorsun?",
            "ans": {"C": "C", "C++": "C++", "Python": "Python", "Java": "Java", "C#": "C#", "Common": "Genel"},
        }
        self.level = {
            "ask": " dilini hangi seviyede biliyorsun?",
            "ans": {"Beginner": "Başlangıç", "Experienced": "Orta", "Advanced": "İleri"},
        }
        self.lang = {
            "ask": "Kaynaklar için dil tercihin?",
            "ans": {
                "Turkish": "Yalnızca Türkçe kaynaklar",
                "English": "Yalnızca İngilizce kaynaklar",
                "TRENG": "Hem Türkçe hem İngilizce kaynaklar",
            },
        }
        self.resources = {
            "ask": "Nasıl bir kaynak arıyorsun?",
            "ans": {
                "Ebooks": "İndirilebilen Kaynaklar",
                "Links": "Videolar ve Faydalı Linkler",
                "Books": "Kitap Önerileri",
            },
        }


questions = Question()


def slicer(button_list: List[InlineKeyboardButton], size: int) -> list:
    return [button_list[i : i + size] for i in range(0, len(button_list), size)]


def make_buttons(answers: dict, size: int, back: str) -> List[InlineKeyboardButton]:
    buttons = [InlineKeyboardButton(text=v, callback_data=k) for k, v in answers]
    buttons = slicer(buttons, size)

    if back:
        back_button: InlineKeyboardButton = InlineKeyboardButton(text="Geri", callback_data=back)
        buttons.append([back_button])

    return buttons


def user_exists(first_name: str, last_name: str, username: str, user: User):
    return all(
        [
            first_name in [i.first_name for i in user.userinfo],
            last_name in [i.last_name for i in user.userinfo],
            username in [i.username for i in user.userinfo],
        ]
    )


def save_user(from_user: PyroUser, tags: dict, books: list = []):
    user: User = session.query(User).filter(User.user_id == str(from_user.id)).first()
    if not user:
        user = User(user_id=from_user.id)

    user_history = History(
        user_id=user.id,
        date=datetime.now(),
        history={"tags": tags, "books": books},
    )
    user.history.append(user_history)

    if not user_exists(from_user.first_name, from_user.last_name, from_user.username, user):
        user_info = UserInfo(
            user_id=from_user.id,
            first_name=from_user.first_name,
            last_name=from_user.last_name,
            username=from_user.username,
        )
        user.userinfo.append(user_info)

    session.commit()