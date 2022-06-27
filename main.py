from interface import App

try:
    app = App()
    app.run()
except Exception as err:
    print(f'發生原因:{err}')
