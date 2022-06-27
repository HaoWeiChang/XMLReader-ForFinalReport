import os
import sys
from rich.console import Console
from patent import Patent, get_stop_word
from rich.progress import track


class App:
    def __init__(self) -> None:
        self.console = Console()
        self.patents = [Patent]

    def run(self) -> None:
        try:
            while True:
                self.__clean_display()
                mode = self.__choose_menu()
                self.__clean_display()
                self.__get_file()
                self.__controller(mode)
                os.system('pause')
        except KeyboardInterrupt:
            self.__clean_display()
            print('結束')
            sys.exit()
        except ValueError:
            self.__clean_display()
            print('請輸入數字')
            os.system('pause')
            self.run()

    def __controller(self, mode: int) -> None:
        if mode == 3:
            res = self.__find_text_match()
            return self.__print_higher_match(res)
        patent = self.__choose_file()

        if mode == 0:
            return self.__print_save(patent)
        elif mode == 1:
            return self.__print_keywords(patent)
        elif mode == 2:
            return self.__print_combine_keywords(patent)
        elif mode == 4:
            return self.__get_common_word(patent)

    def __choose_menu(self) -> int:
        modes = ['匯出格式化文字檔', '專利文章關鍵字', '專利文章組合關鍵字', '搜尋高度相關文章', '顯示已刪除常見字']
        for i, m in enumerate(modes):
            self.console.print(i, m)
        mode = int(input('輸入數字(Ctrl + C 離開程式): '))
        if mode < 0 or mode > len(modes):
            return self.console.print('範圍0~3')
        return mode

    def __choose_file(self) -> Patent:
        for i, file in enumerate(self.patents):
            self.console.print('{:3d} {:10s}'.format(i, file.name))
        select = int(self.console.input('請輸入數字:'))
        if select < 0 or select > len(self.patents):
            print(f'請輸入範圍0~{len(self.patents)}\n')
            self.__choose_file()
        return self.patents[select]

    def __print_save(self, patent: Patent):
        for _ in track(range(100), description='Saving.........'):
            patent.format_save()
        self.console.print(
            f'\n\n完成存檔,檔名:{patent.name}.txt', style="green bold")
        return

    def __print_keywords(self, patent: Patent):
        keywords = []
        num = input('輸入需顯示關鍵字數量:')
        num = 20 if num == '\n' or num == ''else int(num)
        self.__clean_display()
        for _ in track(range(100), description='Finding KeyWords......'):
            keywords = patent.get_keywords(num)
        if keywords != 0:
            self.console.print(f'檔名:{patent.name}')
            self.console.print(
                '{:3s} {:10s} {:3s}'.format('index', 'keyword', 'total'))
            for i, v in enumerate(keywords):
                self.console.print(
                    '{:3d} {:10s} {:3d}'.format(i, v[0], v[1]))
        return

    def __print_combine_keywords(self, patent: Patent):
        keywords = []
        lenth = int(input('請輸入關鍵字組合數(2~5字):'))
        show = input('輸入需顯示的組合關鍵字數量:')
        show = 20 if show == '' else int(show)
        self.__clean_display()
        for _ in track(range(10), description='尋找組合關鍵字'):
            keywords = patent.get_combine_keywords(lenth, show)
        if keywords != 0:
            self.console.print(f'檔名:{patent.name}')
            self.console.print(
                '{:5s} {:50s} {:5s}'.format('index', 'keyword', 'total'))
            for i, v in enumerate(keywords):
                self.console.print(
                    '{:5d} {:50s} {:5d}'.format(i, v[0], v[1]))

    def __find_text_match(self) -> list:
        text = input('請輸入文字:')
        total = 0
        res = []

        for i in self.patents:
            match = i.find_text_match(text)
            if match[2]:
                total += match[2]
                res.append(match)

        res.sort(key=lambda tup: tup[2], reverse=True)
        return (res, total)

    def __print_higher_match(self, matchs):
        if len(matchs[0]):
            while True:
                self.__clean_display()
                self.console.print(
                    '{:5s} {:20s} {:3s}'.format('index', '檔名', '匹配度'))
                for i, v in enumerate(matchs[0]):
                    self.console.print(
                        '{:5d} {:20s} {:1.2f}%'.format(i, v[0], v[2] / matchs[1]))
                num = input('輸入你想看的匹配內容(輸入 n 離開此畫面):')
                if num in ['n', 'N']:
                    return
                self.__print_match_detail(matchs[0][int(num)])
                os.system('pause')
        else:
            self.__clean_display()
            return self.console.print('未找到匹配文字')

    def __print_match_detail(self, detal):
        self.__clean_display()
        self.console.print(f'檔名:{detal[0]}')
        for i, v in enumerate(detal[1]):
            self.console.print(i, v)
        return

    def __get_file(self) -> None:
        f = []
        for (dirpath, _, filenames) in os.walk(os.getcwd()):
            for name in filenames:
                if name.endswith(".XML"):
                    xml = Patent(str(os.path.join(dirpath, name)))
                    f.append(xml)
        self.patents = f

    def __get_common_word(self, patent: Patent) -> None:
        self.__clean_display()
        commons_word = get_stop_word()
        self.console.print(f'檔名:{patent.name}')
        self.console.print('以下為已刪除常見字')
        for i in commons_word:
            self.console.print(i)
        return

    def __clean_display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
