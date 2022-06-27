from interface import App

try:
    app = App()
    app.run()
except Exception:
    print('發生不明原因')
