from enum import Enum
from typing import List

import requests
from pydantic import BaseModel


class Order(Enum):
    RELEVANCE = 1  # order by most relevance
    PUBLISHED = 2  # order by latest published
    DOWNLOADS = 3  # order by most downloads
    CITATIONS = 4  # order by most citations


class CnkiRequest(BaseModel):
    searchType: str = "MulityTermsSearch"
    ParamIsNullOrEmpty: str = "false"
    Islegal: str = "false"
    Theme: str | None = None
    ExcludeField: str | None = None
    Order: int | None = Order.RELEVANCE.value
    Page: int | None = 1
    ArticleType: int | None = 0
    Originate: str | None = None
    PublishTimeBegin: str | None = None
    PublishTimeEnd: str | None = None


class Article(BaseModel):
    title: str
    publishTime: str
    downloadCount: int
    quoteCount: int
    keyWord: str | None


class CnkiResponse(BaseModel):
    pageIndex: int
    articleList: List[Article]
    totalCount: int
    totalPageCount: int


def fetch(url, param):
    try:
        response = requests.post(url, param).json()
    except requests.exceptions.JSONDecodeError:
        response = fetch(url, param)
    res = CnkiResponse.model_validate(response)
    return res


def filter(articles):
    """filter those results that are not technical articles"""
    res = []
    for e in articles:
        p = e.model_dump()
        kw, dc = p["keyWord"], p["downloadCount"]
        if len(kw.split(";")) < 3 or dc == 0:
            continue
        res.append(p)
    return res
