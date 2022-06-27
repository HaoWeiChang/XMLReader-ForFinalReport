from interface import App

try:
    app = App()
    app.run()
except Exception:
    print('發生不明原因')

# f = get_file()
# xml = Patent(f[0])
# xml.format_save()
# xml.find_test(2)
# print('-'*10)
# print(xml.get_keywords())
# print(xml.get_combine_keywords())
