import os
import re
from typing import Any, List
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from patent import Patent


def get_file() -> List[str]:
    f = []
    for (dirpath, _, filenames) in os.walk(os.getcwd()):
        for name in filenames:
            if name.endswith(".XML"):
                f.append(os.path.join(dirpath, name))
    return f


def find_keyword(xml: Patent, num: int = None) -> list[tuple[Any, int]]:
    wordList = []
    text = xml.soup.get_text()
    text = re.sub(r'[0-9]+', '', text)
    en_stops = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    token = tokenizer.tokenize(text)
    for word in token:
        if word.lower() not in en_stops and len(word) > 1:
            wordList.append(word)
    fdist = FreqDist(wordList)
    return fdist.most_common(num)


def find_combine_keyword(xml: Patent):
    text = xml.soup.get_text()
    keyList = find_keyword(xml)
    total = [t[1] for t in keyList]
    mean = sum(total)//len(total)
    keyWords = [i for i in keyList if i[1] > mean]
    combineList = []
    for i in keyWords:
        for j in keyWords:
            key = f'{i[0]} {j[0]}'
            find_pattern = re.compile(key, re.I)
            match = find_pattern.findall(text)
            if len(match) != 0:
                combineList.append((key, len(match)))
    combineList.sort(key=lambda tup: tup[1], reverse=True)
    print(combineList)


f = get_file()
xml = Patent(f[0])
xml.format_save()
find_combine_keyword(xml)
# print(find_keyword(xml))
