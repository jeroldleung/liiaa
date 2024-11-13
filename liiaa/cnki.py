import datetime
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
    PublishTimeBegin: str = str(datetime.datetime.now().year - 1) + "年"
    PublishTimeEnd: str = "不 限"


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


class CnkiService:
    def __init__(self, originate):
        self.url = "https://search.cnki.com.cn/api/search/listresult"
        self.request_data = CnkiRequest(Originate=originate).model_dump()

    def fetch(self):
        try:
            response = requests.post(self.url, self.request_data).json()
        except requests.exceptions.JSONDecodeError:
            response = self.fetch()
        res = CnkiResponse.model_validate(response)
        return res

    def filter(self, articles):
        """filter articles and clean the data"""
        res = []
        for e in articles:
            p = e.model_dump()
            kw, dc = p["keyWord"], p["downloadCount"]

            # drop the informal articles
            if len(kw.split(";")) < 3 or dc == 0:
                continue

            # turn the string of keyword to a list
            nkw = []
            for w in kw.split(";"):
                if w == "":
                    continue
                nkw.append(w)

            p["keyWord"] = nkw
            res.append(p)
        return res

    def get(self):
        data = []
        # fetch for the first time,
        # add the result to the data,
        # and get the total page size
        response = self.fetch()
        data += self.filter(response.articleList)
        pz = response.totalPageCount

        # loop over the page and add the result
        for i in range(2, pz):
            self.request_data["Page"] = i
            response = self.fetch()
            data += self.filter(response.articleList)
        return data
