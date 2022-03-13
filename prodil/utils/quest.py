from typing import Dict, List, Tuple, Union

from pyrogram.types import InlineKeyboardButton as InlineKB

from prodil.BotConfig import api
from prodil.utils.messages import NOT_SELECTED


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
        # "BK": "Kitap Önerileri",
        "DC": "İndirilebilen Kaynaklar",
        "LN": "Videolar ve Faydalı Linkler",
    }


class Category:
    QUESTION = "Hangi programlama dili ile ilgileniyorsun?"

    def __init__(self):
        self.categories = api.get_categories()

    def update_answers(self):
        self.categories = api.get_categories()

    @property
    def ANSWER(self):
        return {i["name"]: i["name"] for i in self.categories}


class Question:
    local = Local()
    content = Content()
    category = Category()

    LEVEL = "level"
    LOCAL = "local"
    CONTENT = "content"
    CATEGORY = "category"

    def get_question(self, question: str) -> str:
        return getattr(self, question).QUESTION

    def get_answer(self, question: str) -> Dict[str, str]:
        return getattr(self, question).ANSWER

    def get_choices(self, question: str) -> Tuple[str, Dict[str, str]]:
        return self.get_question(question), self.get_answer(question)

    def update_answers(self):
        self.category.update_answers()


questions = Question()


def slicer(button_list: List[InlineKB], size: int) -> List[List[InlineKB]]:
    return [button_list[i : i + size] for i in range(0, len(button_list), size)]


def make_buttons(
    answer: Dict[str, str], size: int, back: Union[str, bool]
) -> List[List[InlineKB]]:
    buttons = [InlineKB(text=v, callback_data=k) for k, v in answer.items()]
    buttons = slicer(buttons, size)

    if back:
        back_button: InlineKB = InlineKB(text="Geri", callback_data=back)
        buttons.append([back_button])

    return buttons


def content_buttons(num: int) -> List[List[InlineKB]]:
    buttons = [
        InlineKB(text=f"{NOT_SELECTED} {i+1}", callback_data=str(i + 1))
        for i in range(num)
    ]
    buttons = slicer(buttons, 4)
    return buttons
