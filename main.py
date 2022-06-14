from typing import List
from bs4 import BeautifulSoup
from os import walk
import os
import re


def show_file() -> List[str]:
    f = []
    for (dirpath, _, filenames) in walk(os.getcwd()):
        for name in filenames:
            if name.endswith(".XML"):
                f.append(os.path.join(dirpath, name))
    for i, v in enumerate(f):
        print(f'{i}:{v}')
    return f


class XmlFile:
    def __init__(self, path: str) -> None:
        self.name = "".join(path.split('\\')[-1])
        self.path = path
        self.description = ""
        self.keyword = []
        self.combineword = []
        pass

    def answer_a(self) -> None:
        contents = open(self.path, "r").read()
        soup = BeautifulSoup(contents, 'lxml')
        data_grant = soup.find("us-bibliographic-data-grant")
        abstract = soup.find("abstract")
        description = soup.find("description")
        texts = re.sub('<[^<]+>', "", open(self.path, "r").read())

    def answer_b_c(self):
        print(self.description)


if __name__ == '__main__':
    f = show_file()
    a = int(input("input number:"))
    xml = XmlFile(f[a])
    xml.answer_a()
    # xml.answer_b_c()
