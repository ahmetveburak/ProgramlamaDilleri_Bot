from pyrogram import filters
from typing import List
from prodil.utils.helpers import questions


def filterList(filter_data) -> List[str]:
    myFilter = list(getattr(questions, filter_data)["ans"].keys())

    go_back = {
        "None": "p_lang",
        "p_lang": "level",
        "level": "lang",
        "lang": "resources",
        "resources": "None",
    }

    myFilter.append(go_back[filter_data])
    return myFilter


plang_filter = filters.create(lambda _, __, query: query.data in filterList("p_lang"))
level_filter = filters.create(lambda _, __, query: query.data in filterList("level"))
local_filter = filters.create(lambda _, __, query: query.data in filterList("lang"))
resource_filter = filters.create(lambda _, __, query: query.data in filterList("resources"))

plang = filters.create(lambda _, __, query: query.data == "p_lang")
common = filters.create(lambda _, __, query: query.data == "Common")
