from typing import Dict, List, Tuple, Union

from pyrogram.types import InlineKeyboardButton as InlineKB


class Question:
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
            "__": "Hem Türkçe hem İngilizce kaynaklar",
        }

    class Content:
        QUESTION = "Nasıl bir kaynak arıyorsun?"
        ANSWER = {
            "BK": "Kitap Önerileri",
            "DC": "İndirilebilen Kaynaklar",
            "LN": "Videolar ve Faydalı Linkler",
        }

    class Category:
        QUESTION = "Hangi programlama dili ile ilgileniyorsun?"
        ANSWER = {
            "C": "C",
            "C++": "C++",
            "Python": "Python",
            "Java": "Java",
            "C#": "C#",
            "Common": "Genel",
        }

    LEVEL = "level"
    LOCAL = "local"
    CONTENT = "content"
    CATEGORY = "category"

    def get_question(self, question: str) -> str:
        return getattr(self, question.title()).QUESTION

    def get_answer(self, question: str) -> Dict[str, str]:
        return getattr(self, question.title()).ANSWER

    def get_choices(self, question: str) -> Tuple[str, Dict[str, str]]:
        return self.get_question(question), self.get_answer(question)


quest = Question()


def slicer(button_list: List[InlineKB], size: int) -> List[List[InlineKB]]:
    return [button_list[i : i + size] for i in range(0, len(button_list), size)]


def make_buttons(answer: Dict[str, str], size: int, back: Union[str, bool]) -> List[List[InlineKB]]:
    buttons = [InlineKB(text=v, callback_data=k) for k, v in answer.items()]
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
