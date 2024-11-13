import json

from liiaa.cnki import CnkiService
from liiaa.wordcloud import KeywordCloud


def main():
    # fetch articles of journals related to lighting from cnki,
    # store the information to a jsonl file for further analysis
    data = []
    try:
        with open("./data/articles.jsonl", "r") as file:
            for line in file:
                data.append(json.loads(line))
    except FileNotFoundError:
        cll = CnkiService(originate="中国照明电器")
        ciej = CnkiService(originate="照明工程学报")
        data += cll.get()
        data += ciej.get()
        with open("./data/articles.jsonl", "w") as file:
            for e in data:
                file.write(json.dumps(e, ensure_ascii=False) + "\n")

    # count the frequencies of articles keyword and draw a wordcloud
    kws = [e["keyWord"] for e in data]
    wc = KeywordCloud(font_path="./font/SimHeiBold.ttf", width=1200, height=600)
    wc.generate(kws)
    wc.show()


if __name__ == "__main__":
    main()
