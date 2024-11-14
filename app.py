import json

from liiaa.cnki import CnkiService
from liiaa.patent import PatentHubService
from liiaa.wordcloud import KeywordCloud


#
# load data from the file, if it doesn't exist,
# call the service to fetch data from the internet，
# and store the results to a json line file
#
def get_data(fpath, service):
    data = []
    try:
        with open(fpath, "r") as file:
            for line in file:
                data.append(json.loads(line))
    except FileNotFoundError:
        data = service.get()
        with open(fpath, "w") as file:
            for e in data:
                file.write(json.dumps(e, ensure_ascii=False) + "\n")
    return data


def main():
    a_data, p_data = [], []

    # article data from each journals
    a_data += get_data(
        "./data/a-ChinaLight&Lighting.jsonl", CnkiService(originate="中国照明电器")
    )
    a_data += get_data(
        "./data/a-ChinaIlluminatingEngineeringJournal.jsonl",
        CnkiService(originate="照明工程学报"),
    )

    # patent data from each company
    p_data += get_data(
        "./data/p-OceansKingLighting.jsonl",
        PatentHubService(applicant="海洋王照明科技股份有限公司"),
    )

    # count the frequencies of articles keyword and draw a wordcloud
    kws = [e["keyWord"] for e in a_data]
    wc = KeywordCloud(font_path="./font/SimHeiBold.ttf", width=1200, height=600)
    wc.generate(kws)
    wc.show()


if __name__ == "__main__":
    main()
