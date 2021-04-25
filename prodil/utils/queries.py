from typing import Union, List
from prodil.models.model import (
    Tag,
    session,
    Document,
    doc_tag_table,
    Link,
    link_tag_table,
    Book,
    book_tag_table,
)
from sqlalchemy import func


class QueryHistory:
    def __init__(self):
        self.hist: dict = {}

    def add_user(self, uid: int) -> None:
        self.hist.update(
            {
                uid: {
                    "query": {"p_lang": [], "level": [], "lang": [], "res": []},
                    "download": [],
                    "res_text": "",
                }
            }
        )

    def del_user(self, uid: int) -> None:
        del self.hist[uid]

    def add_data(self, uid: int, key: str, data: str) -> None:
        if data == "TRENG":
            self.hist[uid]["query"][key].extend(["Turkish", "English"])
        else:
            self.hist[uid]["query"][key].append(data)

    def show_history(self, uid: int) -> None:
        print(f"UserID: {uid} - Query: {self.hist[uid]['query']}")

    def go_back(self, uid: int, key: str) -> None:
        self.hist[uid]["query"][key].clear()

    def tags(self, uid: int) -> dict:
        query = self.hist[uid]["query"]
        return query["p_lang"] + query["lang"] + query["level"]

    def get_query(self, model: Union[Document, Link, Book], tag_ids: list) -> List[Union[Document, Link, Book]]:
        if model == Document:
            document_ids = (
                session.query(doc_tag_table.c.document_id)
                .filter(doc_tag_table.c.tag_id.in_(tag_ids))
                .group_by(doc_tag_table.c.document_id)
                .having(func.count(doc_tag_table.c.tag_id) == 3)
                .all()
            )
            return (
                session.query(Document)
                .filter(Document.id.in_(document_ids), Document.enabled == True)
                .order_by(-Document.rating)
                .all()
            )

        elif model == Link:
            link_ids = (
                session.query(link_tag_table.c.link_id)
                .filter(link_tag_table.c.tag_id.in_(tag_ids))
                .group_by(link_tag_table.c.link_id)
                .having(func.count(link_tag_table.c.tag_id) == 3)
                .all()
            )
            return session.query(Link).filter(Link.id.in_(link_ids), Link.enabled == True).order_by(-Link.rating).all()

        else:
            book_ids = (
                session.query(book_tag_table.c.book_id)
                .filter(book_tag_table.c.tag_id.in_(tag_ids))
                .group_by(book_tag_table.c.book_id)
                .having(func.count(book_tag_table.c.tag_id) == 3)
                .all()
            )
            return session.query(Book).filter(Book.id.in_(book_ids), Book.enabled == True).order_by(-Book.rating).all()

    def get_res(self, uid: int, tags: list) -> str:
        tag_ids = [i[0] for i in session.query(Tag.id).filter(Tag.name.in_(tags)).all()]
        search = self.hist[uid]["query"]["res"][0]

        not_found = "Aramalarınıza uygun kaynak bulunamadı. Botta bulunmasının iyi olacağını düşündüğünüz kaynaklar var ise [kaynak formunu](https://forms.gle/bgoVUXKU81d1Cj5y6) kullanarak bize iletebilirsiniz."
        result: list = []

        if search == "Ebooks":
            docs = self.get_query(Document, tag_ids)
            self.hist[uid]["download"] = docs

            for i, doc in enumerate(docs):
                authors = [f"{i.first_name} {i.last_name}" for i in doc.authors]
                result.append(f"{i+1}. **{doc.name}**\n- __{', '.join(authors)}__\n__{doc.note}__\n\n")

            message = "**İndirmek istediğiniz kitapların numaralarını aralarında boşluk bırakarak yazınız.**\n__Faydalı olması dileğiyle..__"
            return "".join(result) + message if result else not_found

        elif search == "Links":
            links = self.get_query(Link, tag_ids)
            for i, link in enumerate(links):
                authors = [f"{i.first_name} {i.last_name}" for i in link.authors]
                result.append(f"**[{i+1}. {link.name}]({link.path})**\n- __{', '.join(authors)}__\n__{link.note}__\n\n")

            return "".join(result) if result else not_found

        else:
            books = self.get_query(Book, tag_ids)
            for i, book in enumerate(books):
                authors = [f"{i.first_name} {i.last_name}" for i in book.authors]
                result.append(f"{i+1}. **{book.name}**\n- __{', '.join(authors)}__\n__{book.note}__\n\n")

            return "".join(result) if result else not_found


# TODO
class Resource:
    def __init__(self):
        self.res: dict = {}
