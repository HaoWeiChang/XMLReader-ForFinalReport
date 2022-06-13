from bs4 import BeautifulSoup


class XmlFile:
    def __init__(self, path: str) -> None:
        self.path = path
        self.description = ""
        self.keyword = []
        self.combineword = []
        pass

    def read(self) -> None:
        print(self.path)
        with open(self.path, "r") as xml:
            contents = xml.read()
            text = BeautifulSoup(contents, 'xml')
            self.description = text.find_all('description')
        xml.close()

    def print(self):
        print(self.description)


if __name__ == '__main__':
    xml = XmlFile(
        "c:/Users/406/Downloads/UTIL08438/UTIL08438/US08438662-20130514/US08438662-20130514.XML")
    xml.read()
    xml.print()
