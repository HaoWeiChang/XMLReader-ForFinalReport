from typing import List
from bs4 import BeautifulSoup
from os import walk 
import os 

def show_file() -> List[str]:
    f = []
    for (dirpath,_,filenames) in walk(os.getcwd()):
        for name in filenames: 
            if name.endswith(".XML"):
                f.append(os.path.join(dirpath,name))
    for i,v in enumerate(f):
        print(f'{i}:{v}')
    return f

class XmlFile:
    def __init__(self, path: str) -> None:
        self.path = path
        self.description = ""
        self.keyword = []
        self.combineword = []
        pass

    def read(self) -> None:
        with open(self.path, "r") as xml:
            contents = xml.read()
            text = BeautifulSoup(contents, 'xml')
            self.description = text.find_all('description')
        xml.close()

    def print(self):
        print(self.description)


if __name__ == '__main__':
    f = show_file()
    a = int(input())
    xml = XmlFile(f[a])
    xml.read()
    xml.print()
