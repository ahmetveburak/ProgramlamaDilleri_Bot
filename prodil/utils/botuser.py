from collections import defaultdict
from typing import Dict

from pyrogram.types import User

from prodil.utils.quest import quest
from pyrogram.types import InlineKeyboardButton as InlineKB
from math import ceil


class UserNavigation(object):
    query_order = (None, "category", "level", "local", "content", None)

    def __init__(self, user: User):
        self.id = getattr(user, "id")
        self.username = getattr(user, "username")
        self.first_name = getattr(user, "first_name")
        self.last_name = getattr(user, "last_name")
        self.content_list = []
        self.query = {
            quest.CATEGORY: [],
            quest.LEVEL: [],
            quest.LOCAL: [],
            quest.CONTENT: [],
        }

        self.page = 1
        self.all_page = 0
        self.respons = {}
        self.choices = {}

    def action(self, data: str, question: str = None) -> None:
        print(data)
        idx = self.query_order.index(question)
        last = self.query_order[idx + 1]
        if last == data:
            self.query[last].clear()
        else:
            self.query[question].append(data)

    def set_page_data(self, content):
        self.choices.update({self.page: content})

    def get_data(self):
        return self.choices.get(self.page)

    def get_response(self):
        return self.respons.get(self.page)

    def get_page_data(self, page):
        return self.choices.get(page)

    def get_buttons(self, data, download: bool = False):
        total = data["count"]
        next_page = "next" if data["next"] else "None"
        prev_page = "prev" if data["previous"] else "None"

        buttons = [
            [
                InlineKB(text="<", callback_data=prev_page),
                InlineKB(text=f"{self.page}/{ceil(total / 8)}", callback_data="add"),
                InlineKB(text=">", callback_data=next_page),
            ],
        ]
        if download:
            buttons.append([InlineKB(text="Indir", callback_data="download")])

        return buttons

    def get_resources(self):
        # TODO Need Refactor
        pages = self.respons.keys()
        selected_res = defaultdict(list)

        for page in pages:
            for buttons in self.choices.get(page):
                for button in buttons:
                    if "🟢" in button.text:
                        selected_res[page].append(button.callback_data)

        result = []
        for page in pages:
            resp = self.respons.get(page).get("results")
            result.extend([resp[int(i) - 1] for i in selected_res[page]])

    @property
    def category(self):
        return self.query[quest.CATEGORY][0]

    @property
    def level(self):
        return self.query[quest.LEVEL][0]

    @property
    def local(self):
        return self.query[quest.LOCAL][0]

    @property
    def content(self):
        return self.query[quest.CONTENT][0]

    @property
    def query_args(self):
        return {
            quest.LEVEL: self.level,
            quest.LOCAL: self.local,
            quest.CONTENT: self.content,
            quest.CATEGORY: self.category,
            "page": self.page,
        }

    def parse_response(self):
        """
        :return: current page results
        """
        return "\n".join(
            [f"{i}. {doc['name']}" for i, doc in enumerate(self.respons[self.page]["results"], start=1)],
        )


user_list: Dict[int, UserNavigation] = {}
