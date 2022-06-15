from typing import List
from bs4 import BeautifulSoup, NavigableString, Tag
from os import walk
import os
import re


def get_file() -> List[str]:
    f = []
    for (dirpath, _, filenames) in walk(os.getcwd()):
        for name in filenames:
            if name.endswith(".XML"):
                f.append(os.path.join(dirpath, name))
    return f


class XmlFile:
    def __init__(self, path: str) -> None:
        self.name = "".join(path.split('\\')[-1])
        self.path = path
        self.content = ""
        pass

    def answer_a(self) -> None:
        xml_text = open(self.path, "r").read()
        soup = BeautifulSoup(xml_text, 'lxml')
        data_grant = soup.find("us-bibliographic-data-grant")
        abstract = soup.find("abstract")
        description = soup.find("description")
        self.__format_data_grant(data_grant)

    def __format_data_grant(self,
                            data_grant: Tag | NavigableString | None):
        """
        TODO:
            "publication-reference" : Done
            "application-reference"
            "us-application-series-code"
            "us-term-of-grant"
            "classifications-ipcr"
            "classification-national"
            "invention-title"
            "us-references-cited"
            "number-of-claims", "us-exemplary-claim"
            "us-field-of-classification-search"
            "us-related-documents"
            "us-parties"
            ""
        """
        pubRef = data_grant.find("publication-reference")
        appRef = data_grant.find("application-reference")
        print(self.__format_docID(appRef))

    def __formate_docIDs(self, docIDs: List[Tag] | List[NavigableString]):
        res = []
        for tag in docIDs:
            res.append(self.__format_docID(tag))
        return res

    def __format_docID(self, docID: Tag | NavigableString):
        __country = docID.find("country")
        __doc_number = docID.find("doc-number")
        __kind = docID.find("kind")
        __date = docID.find("date")
        country = __country.text if __country else ""
        doc_number = __doc_number.text if __doc_number else ""
        kind = __kind.text if __kind else ""
        date = __date.text if __date else ""

        return f'{country}{int(doc_number)}{kind} :: {date}'


if __name__ == '__main__':
    f = get_file()
    # a = int(input("input number:"))
    xml = XmlFile(f[0])
    xml.answer_a()
    # xml.answer_b_c()
