from pyrogram import filters
from prodil.models.model import session, Questions
from typing import List

questions = session.query(Questions).filter(Questions.id == 1).first()


def filterList(filter_data) -> List[str]:
    myFilter = list(getattr(questions, filter_data)["ans"].keys())
    # myFilter = list(questions[filter_data]["ans"].keys())

    go_back = {
        "None": "p_lang",
        "p_lang": "level",
        "level": "lang",
        "lang": "resources",
        "resources": "Nope",
    }

    myFilter.append(go_back[filter_data])
    return myFilter


lngFilter = filters.create(lambda _, __, query: query.data in filterList("p_lang"))
lvlFilter = filters.create(lambda _, __, query: query.data in filterList("level"))
lclFilter = filters.create(lambda _, __, query: query.data in filterList("lang"))
resFilter = filters.create(lambda _, __, query: query.data in filterList("resources"))

plang = filters.create(lambda _, __, query: query.data == "p_lang")
common = filters.create(lambda _, __, query: query.data == "common")
