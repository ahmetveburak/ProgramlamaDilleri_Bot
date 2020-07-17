from pyrogram import Filters
from prodil.models.model import Questions

questions = Questions.objects().first().question


def filterList(filter_data):
    myFilter = list(questions[filter_data]["ans"].keys())

    go_back = {
        "None": "p_lang",
        "p_lang": "level",
        "level": "lang",
        "lang": "resources",
        "resources": "Nope",
    }

    myFilter.append(go_back[filter_data])
    return myFilter


lngFilter = Filters.create(lambda _, query: query.data in filterList("p_lang"))

lvlFilter = Filters.create(lambda _, query: query.data in filterList("level"))

lclFilter = Filters.create(lambda _, query: query.data in filterList("lang"))

resFilter = Filters.create(lambda _, query: query.data in filterList("resources"))
