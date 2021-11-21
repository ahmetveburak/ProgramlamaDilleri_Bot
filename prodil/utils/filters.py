from typing import List

from pyrogram import filters
from pyrogram.filters import Filter

from prodil.utils.quest import quest


class ProDilFilters:
    """
    Create custom pyrogram filters for questions.
    """

    CATEGORY = "category"
    LEVEL = "level"
    LOCAL = "local"
    CONTENT = "content"
    COMMON = "Genel"

    def _filter_list(self, question: str) -> List[str]:
        """
        :param question: str Set the button datas which trigger the callback
        and append the pervious question data.
        :return: List[str] List of answer keys and additional previous question data
        """
        filter_data = list(quest.get_answer(question).keys())

        previous = {
            self.CATEGORY: self.LOCAL,
            self.LOCAL: self.CONTENT,
        }

        filter_data.append(previous[question])
        return filter_data

    def _create_filter(self, data: str) -> Filter:
        return filters.create(lambda _, __, query: query.data in self._filter_list(data))

    @property
    def category(self) -> Filter:
        return filters.create(lambda _, __, query: query.data == self.CATEGORY)

    @property
    def local(self) -> Filter:
        return self._create_filter(self.CATEGORY)

    @property
    def content(self) -> Filter:
        return self._create_filter(self.LOCAL)

    @property
    def connection(self) -> Filter:
        return filters.create(lambda _, __, query: query.data in ("BK", "DC", "LN"))

    @property
    def numbers(self) -> Filter:
        return filters.create(lambda _, __, query: query.data in list(map(str, range(1, 9))))

    @property
    def next_page(self) -> Filter:
        return filters.create(lambda _, __, query: query.data == "next")

    @property
    def prev_page(self) -> Filter:
        return filters.create(lambda _, __, query: query.data == "prev")

    @property
    def change(self) -> Filter:
        return filters.create(lambda _, __, query: query.data in ["next", "prev"])

    download = filters.create(lambda _, __, query: query.data == "download")

    def lock_download(self):
        self.download = None


bot_filters = ProDilFilters()
