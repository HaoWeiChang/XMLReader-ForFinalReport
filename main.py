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
        self.create()
        pass

    def create(self) -> None:
        """
        TODO:
            "us-bibliographic-data-grant"
            "abstract" : Done
            "description" : Done
            "claims" : Done
        """
        xml_text = open(self.path, "r").read()
        soup = BeautifulSoup(xml_text, 'xml')
        self.data_grant = self.__format_data_grant(
            soup.find("us-bibliographic-data-grant"))
        self.abstract = self.__format_abstract(soup.find("abstract"))
        self.description = self.__format_description(soup.find("description"))
        self.claims = self.__format_claims(
            soup.find("us-claims-statement"), soup.find("claims"))

    def __format_data_grant(self, data_grant: SoupType) -> str:
        def __format() -> str:
            pass

        def __format_name(Tag: SoupType) -> str:
            return f'{Tag.find("first-name").get_text()} {Tag.find("last-name").get_text()}'

        def __format_docID(docID: SoupType) -> str:
            __country = docID.find("country")
            __doc_number = docID.find("doc-number")
            __kind = docID.find("kind")
            __date = docID.find("date")
            country = __country.get_text() if __country else ""
            doc_number = __doc_number.get_text() if __doc_number else ""
            kind = __kind.get_text() if __kind else ""
            date = __date.get_text() if __date else ""

            return f'{country}{int(doc_number)}{kind} :: {date}'

        def __format_title(title: SoupType) -> str:
            return "Title: {}".format(title.get_text().upper())

        def __format_pub_ref(pubRef: SoupType) -> str:
            if pubRef is None:
                return ""
            return "Publication Reference: {}".format(__format_docID(pubRef))

        def __format_app_ref(appRef: SoupType) -> str:
            if appRef is None:
                return ""
            return "Application Reference: {}".format(__format_docID(appRef))

        def __format_term_extension(termExt: SoupType) -> str:
            if termExt is None:
                return ""
            res = "Notice: Subject to any disclaimer, the term of this patent is extended or adjusted under 35 U.S.C. 154(b) by {} days."
            _extension = termExt.find("us-term-extension")
            if _extension is None:
                return res.format(0)
            return res.format(_extension.get_text())

        def __format_class_ipcr(ipcrs: SoupType) -> str:
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

        def __format_class_search(search: SoupType) -> str:
            textList = []
            nationals = search.find_all("classification-national")
            for i in nationals:
                item = i.find("main-classification")
                textList.append(item.get_text())
            res = ", ".join(textList)
            return "Field of Classification Search: {}".format(res)

        def __format_related_doc(related: SoupType) -> str:
            privision = related.find("us-provisional-application")
            prvision_doc = __format_docID(privision)
            publication = related.find("related-publication")
            publication_doc = __format_docID(publication)
            return "Prior Publication Data: {}\nRelated U.S. Application Data: {}".format(publication_doc, prvision_doc)

        def __format_us_parties(parties: SoupType) -> str:
            applicants = parties.findAll("us-applicant")

            pass

        def __format_examiners(examiners: SoupType) -> str:
            primaryStr = "Primary Examiner -- {}".format(
                __format_name(examiners.find("primary-examiner")))
            if examiners.find("assistant-examiner"):
                assistantStr = "Assistant Eaminer -- {}".format(
                    __format_name(examiners.find("assistant-examiner")))
                return f'{primaryStr}\n{assistantStr}'
            return primaryStr
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
            "us-related-documents" : Done
            "us-parties"
            "examiners" : Done
        """

        # print(__format_title(data_grant.find("invention-title")))
        # print(__format_pub_ref(data_grant.find("publication-reference")))
        # print(__format_app_ref(data_grant.find("application-reference")))
        # print(__format_term_extension(
        #     data_grant.find("us-term-of-grant")))
        # print(__format_related_doc(data_grant.find("us-related-documents")))
        # print(__format_class_ipcr(data_grant.find(
        #     "classifications-ipcr")))
        # print(__format_examiners(data_grant.find("examiners")))
        print(__format_class_search(data_grant.find(
            "us-field-of-classification-search")))
        return ""

    def __format_abstract(self, abstract: SoupType) -> str:
        if abstract is None:
            return "Can't find the abstract text!!!!!"
        pTag = abstract.find("p")
        return pTag.get_text() if pTag else ""

    def __format_description(self, description: SoupType) -> str:
        if description is None:
            return "Can't find the description text!!!!!"
        return description.get_text()

    def __format_claims(self, state: SoupType, claims: SoupType) -> str:
        res = state.get_text() if state else "Can't find the claim statement"
        claims = claims.get_text() if claims else "Can't find the claims"
        return res+claims

    def show(self):
        print(self.data_grant)
        print("\n---Abstract---\n")
        print(self.abstract)
        print("\n---Description---\n")
        print(self.description)
        print("\n---Claims---\n")
        print(self.claims)
        pass

    def save(self):
        with open(self.name+".txt", "w") as file:
            file.write(self.data_grant)
            file.write("\n---Abstract---\n")
            file.write(self.abstract)
            file.write("\n---Description---\n")
            file.write(self.description)
            file.write("\n---Claims---\n")
            file.write(self.claims)
        file.close()
        return


if __name__ == '__main__':
    f = get_file()
    xml = XmlFile(f[0])
