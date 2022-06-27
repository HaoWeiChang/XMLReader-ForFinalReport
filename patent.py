from ast import keyword
import re
from signal import raise_signal
from typing import Union
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup, NavigableString, Tag
from regex import A, W

SoupType = Union[Tag, NavigableString, int]


class Patent:
    def __init__(self, path: str) -> None:
        self.name = "".join(path.split('\\')[-1])
        self.path = path
        self.soup = self.__readSoup()
        self.keywords = []
        self.combine_keyword = []

    def __readSoup(self) -> BeautifulSoup:
        xml_text = open(self.path, "r").read()
        return BeautifulSoup(xml_text, 'xml')

    def format_save(self) -> None:
        """
        TODO:
            "us-bibliographic-data-grant"
            "abstract" : Done
            "description" : Done
            "claims" : Done
        """
        res = []
        res.append(self.__format_data_grant(
            self.soup.find("us-bibliographic-data-grant")))
        res.append(self.__format_abstract(self.soup.find("abstract")))
        res.append(self.__format_description(self.soup.find("description")))
        res.append(self.__format_claims(
            self.soup.find("us-claim-statement"), self.soup.find("claims")))
        contents = "\n\n".join(res)
        with open(self.name+".txt", "w", encoding='UTF-8') as file:
            file.write(contents)
        file.close()

    def __format_data_grant(self, data_grant: SoupType) -> str:
        def __format_name(Tag: SoupType) -> str:
            firstTag = Tag.find("first-name")
            lastTag = Tag.find("last-name")
            if firstTag is None or lastTag is None:
                return ""
            first = firstTag.get_text()
            last = lastTag.get_text()
            return f'{first} {last}'

        def __format_address(Tag: SoupType) -> str:
            address = []
            cityTag = Tag.find("city")
            stateTag = Tag.find("state")
            countryTag = Tag.find("country")
            if cityTag:
                address.append(cityTag.get_text())
            if stateTag:
                address.append(stateTag.get_text())
            if countryTag:
                address.append(f"({countryTag.get_text()})")
            return ",".join(address)

        def __format_docID(docID: SoupType) -> str:
            __country = docID.find("country")
            __doc_number = docID.find("doc-number")
            __kind = docID.find("kind")
            __date = docID.find("date")
            country = __country.get_text() if __country else ""
            doc_number = __doc_number.get_text() if __doc_number else ""
            kind = __kind.get_text() if __kind else ""
            date = __date.get_text() if __date else ""
            if kind == "" and country == "" and doc_number == "" and kind == "":
                return ""
            return f'{country}{doc_number}{kind} :: {date}'

        def __format_title(title: SoupType) -> str:
            return "Title: {}".format(title.get_text().upper())

        def __format_parties(Tag: SoupType) -> str:
            applicantsList = []
            inventorsList = []
            agentsList = []
            applicants = Tag.find_all("us-applicant")
            inventors = Tag.find_all("inventor")
            agents = Tag.find_all("agent")
            for item in applicants:
                applicantsList.append(__format_name(item))

            for item in inventors:
                inventorsList.append(__format_name(item)+' ' +
                                     __format_address(item))

            for item in agents:
                name = __format_name(item)
                if name != "":
                    agentsList.append(name)
                    continue
                orgname = item.find("orgname")
                if orgname:
                    agentsList.append(orgname.get_text())
            applicantText = ". ".join(applicantsList)
            inventorText = ". ".join(inventorsList)
            agentsText = ". ".join(agentsList)
            return "Applicants:{}\nInventor:{}\nAttorney, Agent, or Firm:{}""".format(applicantText, inventorText, agentsText)

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
            res = []
            ipcrList = ipcrs.find_all("classification-ipcr")
            for ipce in ipcrList:
                dateText = ipce.find("date").get_text()
                section = ipce.find("section").get_text()
                classText = ipce.find("class").get_text()
                subclass = ipce.find("subclass").get_text()
                mainGroup = ipce.find("main-group").get_text()
                subGroup = ipce.find("subgroup").get_text()
                res.append(
                    f'{section}{classText}{subclass} {mainGroup}/{subGroup}  ({dateText})')
            return "Int. Cl. : {}".format(",".join(res))

        def __format_class_national(national: SoupType) -> str:
            res = []
            mainTag = national.find("main-classification")
            res.append(mainTag.get_text()if mainTag else "")
            furthers = national.find_all("further-classification")
            for i in furthers:
                res.append(i.get_text())
            return "U.S.Cl.(USPC):{}".format(",".join(res))

        def __format_class_search(search: SoupType) -> str:
            textList = []
            nationals = search.find_all("classification-national")
            for i in nationals:
                item = i.find("main-classification")
                textList.append(item.get_text())
            res = ",".join(textList)
            return "Field of Classification Search: {}".format(res)

        def __format_related_doc(related: SoupType) -> str:
            publication = related.find("related-publication")
            publication_doc = "Prior Publication Data: {}".format(
                __format_docID(publication))if publication else ""
            privision = related.find("us-provisional-application")
            privision_doc = "Related U.S. Application Data: {}".format(__format_docID(
                privision)) if privision else ""
            return "\n".join([publication_doc, privision_doc])

        def __format_examiners(examiners: SoupType) -> str:
            primaryStr = "Primary Examiner -- {}".format(
                __format_name(examiners.find("primary-examiner")))
            if examiners.find("assistant-examiner"):
                assistantStr = "Assistant Eaminer -- {}".format(
                    __format_name(examiners.find("assistant-examiner")))
                return f'{primaryStr}\n{assistantStr}'
            return primaryStr

        def __format_ref_cited(cited: SoupType):
            formatList = []
            citations = cited.find_all("us-citation")
            for i in citations:
                formatList.append(__format_docID(i))
            formatList = list(filter(None, formatList))
            res = ", ".join(formatList)
            othercits = cited.find_all("othercit")
            othercitList = []
            othercitRes = ""
            if othercits:
                for i in othercits:
                    othercitList.append(i.get_text())
                othercitRes = "\n".join(othercitList)
                res += f"\nOTHER PUBLICATIONS:\n{othercitRes}"
            return "References Cited: {}".format(res)
        """
        TODO:
            "publication-reference" : Done
            "application-reference" : Done
            "us-application-series-code" : Pass
            "us-term-of-grant" : Done
            "classifications-ipcr" : Done
            "classification-national" : Done
            "invention-title" : Done
            "us-references-cited" : Done
            "number-of-claims", "us-exemplary-claim" : Pass
            "us-field-of-classification-search" : Done
            "us-related-documents" : Done
            "us-parties" : Done
            "examiners" : Done
        """
        res = []
        res.append(__format_title(data_grant.find("invention-title")))
        res.append(__format_parties(data_grant.find("us-parties")))
        res.append(__format_pub_ref(data_grant.find("publication-reference")))
        res.append(__format_app_ref(data_grant.find("application-reference")))
        res.append(__format_term_extension(
            data_grant.find("us-term-of-grant")))
        res.append(__format_related_doc(
            data_grant.find("us-related-documents")))
        res.append(__format_class_ipcr(data_grant.find(
            "classifications-ipcr")))
        res.append(__format_examiners(data_grant.find("examiners")))
        res.append(__format_class_national(
                   data_grant.find("classification-national")))
        res.append(__format_class_search(data_grant.find(
            "us-field-of-classification-search")))
        res.append(__format_ref_cited(data_grant.find("us-references-cited")))
        return "\n\n".join(res)

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

    def __find_keywords(self) -> None:
        text = self.soup.get_text()
        en_stops = set(stopwords.words('english'))
        tokenizer = RegexpTokenizer('\\w+[\'\\.]\\w+|[a-zA-Z]+\\d+|[a-zA-Z]+')
        token = tokenizer.tokenize(text)
        fdist = FreqDist(token)
        keywordList = fdist.most_common()
        self.keywords = [word for word in keywordList if word[0].lower()
                         not in en_stops]

    def find_combine_keywords(self, length: int = 2, show: int = 0) -> None:
        if length < 2 or length > 5:
            raise Exception(f'目前僅提供2~5個字組合關鍵字')
        text = self.soup.get_text()
        calculate = {}
        keywords = []
        en_stops = set(stopwords.words('english'))
        tokenizer = RegexpTokenizer('\\w+[\'\\.]\\w+|[a-zA-Z]+\\d+|[a-zA-Z]+')
        lines = list(filter(None, text.split('\n')))
        for line in lines:
            content = tokenizer.tokenize(line.lower())
            no_stop = [w for w in content if w not in en_stops and w != '']
            if len(no_stop) < length:
                continue
            for index in range(0, len(no_stop)-length):
                word = " ".join(no_stop[index:index+length])
                if word not in calculate:
                    calculate[word] = 1
                else:
                    calculate[word] += 1

        for key, values in calculate.items():
            if values > 1:
                keywords.append((key, values))
        keywords.sort(key=lambda tup: tup[1], reverse=True)
        if show < 0 or show > len(keywords):
            raise Exception(f"請輸入範圍0~{len(keywords)}")
        return keywords[:show] if show else keywords[:show]

    def get_keywords(self, num: int = 0):
        if len(self.keywords) == 0:
            self.__find_keywords()
        return self.keywords[:num] if num else self.keywords

    def get_combine_keywords(self, num: int = 0):
        if len(self.keywords) == 0:
            self.__find_keywords()
        if len(self.combine_keyword) == 0:
            self.__find_combine_keywords()
        return self.combine_keyword[:num] if num else self.combine_keyword

    def find_text_match(self, text: str):
        text = self.soup.get_text()
        test = re.findall('\\b{}\\b'.format(text), A, re.M)
        return test


paten_list = list[Patent]
