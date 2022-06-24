import os
from patent import Patent, check_nltk


def get_file() -> list[str]:
    f = []
    for (dirpath, _, filenames) in os.walk(os.getcwd()):
        for name in filenames:
            if name.endswith(".XML"):
                f.append(os.path.join(dirpath, name))
    return f


check_nltk()
f = get_file()
xml = Patent(f[0])
# xml.format_save()
# print(find_combine_keyword(xml))
