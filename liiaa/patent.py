from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel


class PatentHubRequest(BaseModel):
    t: str = "3d6657978949df34c9ababe4dc0fc82ba4dc8144"  # token
    ds: str = "cn"  # data scope, cn is China
    q: str | None = None  # query statement
    p: int | None = None  # page
    ps: int = 20  # page size
    v: int = 1  # version


class PatentHubService:
    def __init__(self, applicant):
        self.url = "https://www.patenthub.cn/api/s"
        self.params = PatentHubRequest().model_dump()
        self.applicant = applicant
        self.t = datetime.now()

    def get(self):
        # construct the query string for searching specific applicant from last year,
        # and fetch data for the first time
        tdate = str(self.t.year) + "-" + str(self.t.month) + "-" + str(self.t.day)
        fdate = self.t + relativedelta(days=1) - relativedelta(years=1)
        fdate = str(fdate.year) + "-" + str(fdate.month) + "-" + str(fdate.day)
        query = f"ap:{self.applicant} AND dd:[{fdate} TO {tdate}]"
        self.params["q"] = query
        xres = requests.get(self.url, self.params).json()

        # combine the patents list of the response,
        # and loop over the page to get the full results
        data = []
        data += xres["patents"]
        pz = xres["totalPages"]
        for i in range(2, pz):
            self.params["p"] = i
            res = requests.get(self.url, self.params).json()
            data += res["patents"]
        return data
