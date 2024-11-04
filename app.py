import asyncio

import pandas as pd

from liiaa.cnki import CnkiRequest, fetch
from liiaa.wordcloud import KeywordCloud

CNKI_SEARCH = "https://search.cnki.com.cn/api/search/listresult"
JOURNALS = ["China Light & Lighting", "China Illuminating Engineering Journal"]
N_PAGES = 20


def main():
    # fetch articles of journals related to lighting from cnki,
    # store useful information to a csv file for further analysis
    try:
        data = pd.read_csv('articles.csv')
    except FileNotFoundError:
        dfs = []
        for journal in JOURNALS:
            for page in range(1, N_PAGES + 1):
                param = CnkiRequest(Originate=journal, Page=page)
                res = asyncio.run(fetch(CNKI_SEARCH, param.model_dump()))
                df = pd.DataFrame.from_dict([p.model_dump() for p in res.articleList])
                dfs.append(df)
        data = pd.concat(dfs)
        data.to_csv('articles.csv')

    # count the frequencies of articles keyword and draw a wordcloud
    kws = data["keyWord"]
    wc = KeywordCloud(font_path="./font/SimHeiBold.ttf", width=1200, height=600)
    wc.generate(kws.to_list())
    wc.show()


if __name__ == "__main__":
    main()
