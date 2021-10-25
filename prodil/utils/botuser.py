from pyrogram.types import User

from prodil.utils.quest import quest


class UserNavigation(object):
    query_order = (None, "category", "level", "local", "content")

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

    def action(self, data: str, question: str = None) -> None:
        idx = self.query_order.index(question)
        last = self.query_order[idx + 1]
        if last == data:
            print("back")
            self.query[last].clear()
        else:
            self.query[question].append(data)

        print(f"Last: {last}, Ques: {question}, Data: {data}")
        print(self.query)

    @property
    def category(self):
        return self.query[quest.CATEGORY][0]
