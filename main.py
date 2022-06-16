from typing import List, Union
from bs4 import BeautifulSoup, NavigableString, Tag
import os


SoupType = Union[Tag, NavigableString, int]


def get_file() -> List[str]:
    f = []
    for (dirpath, _, filenames) in os.walk(os.getcwd()):
        for name in filenames:
            if name.endswith(".XML"):
                f.append(os.path.join(dirpath, name))
    return f


class XmlFile:

    def __init__(self, path: str) -> None:
        self.name = "".join(path.split('\\')[-1])
        self.path = path
        self.data_grant = ""
        self.abstract = ""
        self.description = ""
        self.claims = ""
        pass

    def answer_a(self) -> None:
        """
        TODO:
            "us-bibliographic-data-grant"
            "abstract" : Done
            "description"
            "claims"
        """

        xml_text = open(self.path, "r").read()
        soup = BeautifulSoup(xml_text, 'xml')
        data_grant = soup.find("us-bibliographic-data-grant")
        abstract = soup.find("abstract")
        description = soup.find("description")
        self._format_data_grant(data_grant)
        print(self._format_abstract(abstract))

    def _format_data_grant(self, data_grant: SoupType):
        """
        TODO:
            "publication-reference" : Done
            "application-reference" : Done
            "us-application-series-code" : Pass
            "us-term-of-grant" : Done
            "classifications-ipcr" : Done
            "classification-national"
            "invention-title" : Done
            "us-references-cited"
            "number-of-claims", "us-exemplary-claim"
            "us-field-of-classification-search"
            "us-related-documents"
            "us-parties"
            "examiners"
            ""
        """

        def _format_docID(docID: SoupType):
            __country = docID.find("country")
            __doc_number = docID.find("doc-number")
            __kind = docID.find("kind")
            __date = docID.find("date")
            country = __country.get_text() if __country else ""
            doc_number = __doc_number.get_text() if __doc_number else ""
            kind = __kind.get_text() if __kind else ""
            date = __date.get_text() if __date else ""

            return f'{country}{int(doc_number)}{kind} :: {date}'

        def _format_title(title: SoupType):
            return "Title: {}".format(title.get_text().upper())

        def _format_inventor(inventor: SoupType):
            return

        def _format_pub_ref(pubRef: SoupType):
            if pubRef is None:
                return ""
            return "Publication Reference: {}".format(_format_docID(pubRef))

        def _format_app_ref(appRef: SoupType):
            if appRef is None:
                return ""
            return "Application Reference: {}".format(_format_docID(appRef))

        def _format_term_extension(termExt: SoupType):
            if termExt is None:
                return ""
            res = "Notice: Subject to any disclaimer, the term of this patent is extended or adjusted under 35 U.S.C. 154(b) by {} days."
            _extension = termExt.find("us-term-extension")
            if _extension is None:
                return res.format(0)
            return res.format(_extension.get_text())

        def _format_class_ipcr(ipcrs: SoupType):
            res = "Int. Cl. :{}"
            ipcrtxt = ""
            ipcrList = ipcrs.find_all("classification-ipcr")
            for ipce in ipcrList:
                dateText = ipce.find("date").get_text()
                section = ipce.find("section").get_text()
                classText = ipce.find("class").get_text()
                subclass = ipce.find("subclass").get_text()
                mainGroup = ipce.find("main-group").get_text()
                subGroup = ipce.find("subgroup").get_text()
                ipcrtxt += f'\n\t{section}{classText}{subclass} {mainGroup}/{subGroup}\t({dateText})'
            return res.format(ipcrtxt)

        print(_format_title(data_grant.find("invention-title")))
        print(_format_pub_ref(data_grant.find("publication-reference")))
        print(_format_app_ref(data_grant.find("application-reference")))
        print(_format_term_extension(
            data_grant.find("us-term-of-grant")))
        print(_format_class_ipcr(data_grant.find(
            "classifications-ipcr")))

    def _format_abstract(self, abstract: SoupType):
        pTag = abstract.find("p")
        if abstract is None or pTag is None:
            return "Can't find the abstract text!!!!! pls check abstract use 'p' and inside the xml file"
        text = pTag.get_text()
        return text

    def _format_description(self, description: SoupType):
        pass

    def _format_claims(self, claims: SoupType):
        pass


if __name__ == '__main__':
    f = get_file()
    # a = int(input("input number:"))
    xml = XmlFile(f[0])
    xml.answer_a()
    # xml.answer_b_c()
