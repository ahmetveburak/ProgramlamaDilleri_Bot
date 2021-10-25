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
    NONE = "none"

    def _filter_list(self, question) -> List[str]:
        """
        :param question: str For obtain related answer keys to create filter
        :return: List[str] List of answer keys and additional previous question data
        """
        filter_data = list(quest.get_answer(question).keys())

        previous = {
            self.NONE: self.CATEGORY,
            self.CATEGORY: self.LEVEL,
            self.LEVEL: self.LOCAL,
            self.LOCAL: self.CONTENT,
            self.CONTENT: self.NONE,
        }

        filter_data.append(previous[question])
        return filter_data

    def _create_filter(self, data: str) -> Filter:
        return filters.create(lambda _, __, query: query.data in self._filter_list(data))

    @property
    def category(self) -> Filter:
        return self._create_filter(self.NONE)

    @property
    def level(self) -> Filter:
        return self._create_filter(self.CATEGORY)

    @property
    def local(self) -> Filter:
        return self._create_filter(self.LEVEL)

    @property
    def content(self) -> Filter:
        return self._create_filter(self.LOCAL)

    @property
    def start(self) -> Filter:
        return filters.create(lambda _, __, query: query.data == self.CATEGORY)

    @property
    def common(self) -> Filter:
        return filters.create(lambda _, __, query: query.data == self.COMMON)


bot_filters = ProDilFilters()
