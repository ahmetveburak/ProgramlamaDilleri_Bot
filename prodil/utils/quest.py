# from prodil.models.model import session, History, UserInfo, User
from pyrogram.types import InlineKeyboardButton as InlineKB
from pyrogram.types import User as PyroUser
from datetime import datetime
from typing import Dict, List, Tuple, Union


class Level:
    QUESTION = "dilini hangi seviyede biliyorsun?"
    ANSWER = {
        "BGN": "Başlangıç",
        "EXP": "Orta",
        "PRO": "İleri",
    }


class Local:
    QUESTION = "Kaynaklar için dil tercihin?"
    ANSWER = {
        "TR": "Yalnızca Türkçe kaynaklar",
        "EN": "Yalnızca İngilizce kaynaklar",
    }


class Content:
    QUESTION = "Nasıl bir kaynak arıyorsun?"
    ANSWER = {
        "BK": "Kitap Önerileri",
        "DC": "İndirilebilen Kaynaklar",
        "LN": "Videolar ve Faydalı Linkler",
    }


class Question:
    LEVEL = Level
    LOCAL = Local
    CONTENT = Content

    def __init__(self) -> None:
        self.category = {
            "ask": "Hangi programlama dili ile ilgileniyorsun?",
            "ans": {
                "C": "C",
                "C++": "C++",
                "Python": "Python",
                "Java": "Java",
                "C#": "C#",
                "Common": "Genel",
            },
        }

    def set_local(self):
        # TODO
        # Get categories from API
        pass

    def get_question(self, question: str) -> str:
        return getattr(self, question.upper()).QUESTION

    def get_answer(self, question: str) -> Dict[str, str]:
        return getattr(self, question.upper()).ANSWER

    def get_choices(self, question: str) -> Tuple[str, Dict[str, str]]:
        return self.get_question(question), self.get_answer(question)


def slicer(button_list: List[InlineKB], size: int) -> List[List[InlineKB]]:
    return [button_list[i : i + size] for i in range(0, len(button_list), size)]


def make_buttons(answers: dict, size: int, back: Union[str, bool]) -> List[List[InlineKB]]:
    buttons = [InlineKB(text=v, callback_data=k) for k, v in answers]
    buttons = slicer(buttons, size)

    if back:
        back_button: InlineKB = InlineKB(text="Geri", callback_data=back)
        buttons.append([back_button])

    return buttons


def user_exists(first_name: str, last_name: str, username: str, user):
    return all(
        [
            first_name in [i.first_name for i in user.userinfo],
            last_name in [i.last_name for i in user.userinfo],
            username in [i.username for i in user.userinfo],
        ]
    )


# def save_user(from_user: PyroUser, tags: dict, books: list = []):
#     user: User = session.query(User).filter(User.user_id == str(from_user.id)).first()
#     if not user:
#         user = User(user_id=from_user.id)
#
#     user_history = History(
#         user_id=user.id,
#         date=datetime.now(),
#         history={"tags": tags, "books": books},
#     )
#     user.history.append(user_history)
#
#     if not user_exists(from_user.first_name, from_user.last_name, from_user.username, user):
#         user_info = UserInfo(
#             user_id=from_user.id,
#             first_name=from_user.first_name,
#             last_name=from_user.last_name,
#             username=from_user.username,
#         )
#         user.userinfo.append(user_info)
#
#     session.commit()


# _level = {
#         "ask": " dilini hangi seviyede biliyorsun?",
#         "ans": {
#             "Beginner": "Başlangıç",
#             "Experienced": "Orta",
#             "Advanced": "İleri",
#         },
#     }
#     _local = {
#         "ask": "Kaynaklar için dil tercihin?",
#         "ans": {
#             "Turkish": "Yalnızca Türkçe kaynaklar",
#             "English": "Yalnızca İngilizce kaynaklar",
#             "TRENG": "Hem Türkçe hem İngilizce kaynaklar",
#         },
#     }
#     _content = {
#         "ask": "Nasıl bir kaynak arıyorsun?",
#         "ans": {
#             "Ebooks": "İndirilebilen Kaynaklar",
#             "Links": "Videolar ve Faydalı Linkler",
#             "Books": "Kitap Önerileri",
#         },
#     }
