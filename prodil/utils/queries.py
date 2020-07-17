from datetime import datetime
from prodil.models.model import Documents, Links, Books


class History:
    def __init__(self):
        self.hist: dict = {}

    def add_user(self, uid: int) -> None:
        self.hist.update(
            {uid: {"query": [], "time": datetime.now()}, "res": [], "res_text": ""}
        )

    def add_data(self, uid: int, data: str) -> None:
        self.hist[uid]["query"].append(data)

    def show_history(self, uid: int) -> None:
        print(f"UserID: {uid} - Query: {self.hist[uid]['query']}")

    def go_back(self, uid: int) -> None:
        self.hist[uid]["query"] = self.hist[uid]["query"][0:-2]

    def tags(self, uid: int) -> dict:
        return self.hist[uid]["query"]

    def get_res(self, uid: int) -> str:
        tags = self.hist[uid]["query"]
        resources = None

        not_found = "Kaynak Yok Kardes :("

        if "treng" in tags:
            tags.remove("treng")

        if tags[-1] == "ebooks":
            resources = Documents.objects(tags__all=tags[:-1]).order_by("-rating")

            result = [
                f"{i+1}. **{res.name}**\n- __{', '.join(res.authors)}__\n__{res.note}__\n\n"
                for i, res in enumerate(resources)
            ]

            message = "Lutfen kitaplarin numaralarini bosluk birakarak giriniz"
            self.hist[uid]["res"] = resources
            return "".join(result) + message if result else not_found

        elif tags[-1] == "links":
            resources = Links.objects(tags__all=tags[:-1]).order_by("-rating")

            result = [
                f"**[{i+1}. {res.name}]({res.path})**\n- __{', '.join(res.authors)}__\n__{res.note}__\n\n"
                for i, res in enumerate(resources)
            ]

            self.hist[uid]["res"] = resources
            return "".join(result) if result else not_found

        else:
            resources = Books.objects(tags__all=tags[:-1]).order_by("-rating")

            result = [
                f"{i+1}. **{res.name}**\n- __{', '.join(res.authors)}__\n__{res.note}__\n\n"
                for i, res in enumerate(resources)
            ]

            self.hist[uid]["res"] = resources
            return "".join(result) if result else not_found


# TODO
class Resource:
    def __init__(self):
        self.res: dict = {}

