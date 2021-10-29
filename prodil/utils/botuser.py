from collections import defaultdict
from math import ceil
from typing import Dict, List

from pyrogram.types import InlineKeyboardButton as InlineKB
from pyrogram.types import User

from prodil.utils.quest import quest
from prodil_client.client import api


class UserNavigation(object):
    query_order = (None, "category", "level", "local", "content", None)

    def __init__(self, user: User):
        self.id = getattr(user, "id")
        self.username = getattr(user, "username")
        self.first_name = getattr(user, "first_name")
        self.last_name = getattr(user, "last_name")

        self.page = 1
        self.all_page = 0

        self.respons = {}
        self.choices = {}

        self.category = None
        self.level = None
        self.local = None
        self.content = None

    def action(self, data: str, question: str = None) -> None:
        print(data)

        idx = self.query_order.index(question)
        last = self.query_order[idx + 1]
        if last == data:
            setattr(self, last, None)
            if data == "content":
                self.page = 1
                # self.respons = self.choices = {}
        else:
            setattr(self, question, data)

    def set_page_data(self, content: List[List[InlineKB]]):
        """
        Save keyboard data for current page.
        """
        self.choices.update({self.page: content})

    def get_data(self) -> Dict[int, dict]:
        """
        Get chosen keyboard data for current page.
        """
        return self.choices.get(self.page)

    def get_response(self) -> Dict[int, dict]:
        """
        Get response data for current page.
        """
        return self.respons.get(self.page)

    def get_buttons(self, data):
        """
        Create navigation buttons.
        """
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
        if self.content == "DC":
            buttons.append([InlineKB(text="Indir", callback_data="download")])

        buttons.append([InlineKB(text="Geri", callback_data="content")])

        return buttons

    def get_resources(self):
        """
        Get resources from api with choosen parameters.
        """
        response = self.respons[self.page] = api.get_resources(**self.query_args)
        return response

    def get_documents(self):
        """
        Get choosen documents from choices.
        """
        # TODO Need Refactor
        pages = self.respons.keys()
        selected_res = defaultdict(list)

        for page in pages:
            for buttons in self.choices.get(page)[:2]:
                for button in buttons:
                    if "🟢" in button.text:
                        selected_res[page].append(button.callback_data)

        result = []
        for page in pages:
            resp = self.respons.get(page).get("results")
            result.extend([resp[int(i) - 1] for i in selected_res[page]])

        return result

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
        Parse current page's json response to readable format.
        """
        return "\n".join(
            [f"{i}. {doc['name']}" for i, doc in enumerate(self.respons[self.page]["results"], start=1)],
        )


user_list: Dict[int, UserNavigation] = {}
