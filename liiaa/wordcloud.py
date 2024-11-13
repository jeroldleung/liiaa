import matplotlib.pyplot as plt
from wordcloud import WordCloud


class KeywordCloud:
    def __init__(self, font_path, width, height):
        self.wc = WordCloud(
            font_path=font_path, background_color="white", width=width, height=height
        )

    def generate(self, keywords):
        """counting frequencies of each word in a list of string"""
        frq = {}
        for kws in keywords:
            for w in kws:
                frq[w] = frq.get(w, 0) + 1
        self.wc.generate_from_frequencies(frq)

    def save(self, file_name):
        self.wc.to_file(file_name)

    def show(self):
        plt.imshow(self.wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()
