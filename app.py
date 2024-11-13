import json

from liiaa.cnki import CnkiRequest, fetch, filter
from liiaa.wordcloud import KeywordCloud

CNKI_SEARCH = "https://search.cnki.com.cn/api/search/listresult"
JOURNALS = ["China Light & Lighting", "China Illuminating Engineering Journal"]
N_PAGES = 20


def main():
    # fetch articles of journals related to lighting from cnki,
    # store the information to a jsonl file for further analysis
    data = []
    try:
        with open("articles.jsonl", "r") as file:
            for line in file:
                data.append(json.loads(line))
    except FileNotFoundError:
        with open("articles.jsonl", "w") as file:
            for journal in JOURNALS:
                for page in range(1, N_PAGES + 1):
                    param = CnkiRequest(Originate=journal, Page=page)
                    xres = fetch(CNKI_SEARCH, param.model_dump())
                    res = filter(xres.articleList)
                    for l in res:
                        file.write(json.dumps(l, ensure_ascii=False) + "\n")
                    data += res

    # count the frequencies of articles keyword and draw a wordcloud
    kws = [e["keyWord"] for e in data]
    wc = KeywordCloud(font_path="./font/SimHeiBold.ttf", width=1200, height=600)
    wc.generate(kws)
    wc.show()


if __name__ == "__main__":
    main()
