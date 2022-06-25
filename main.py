import os
from patent import Patent


def get_file() -> list[str]:
    f = []
    for (dirpath, _, filenames) in os.walk(os.getcwd()):
        for name in filenames:
            if name.endswith(".XML"):
                f.append(os.path.join(dirpath, name))
    return f


f = get_file()
xml = Patent(f[0])
# # xml.format_save()
xml.find_test()
# print(xml.get_keywords())
# print(xml.get_combine_keywords())
