# 專利取得與攻防 期末報告
## 初始環境
程式碼有使用變數型別，為了防止執行時出錯，請依照下方版本或使用最新版本

```python
python -V       # Python 3.10.4
pip -V          # pip 22.0.4
```

提供簡易的初始化執行檔，恢復python環境

### Linux : init.bash

```bash
#!/bin/bash

pip install -r requirements.txt

python -m nltk.downloader stopwords
```

### Windows: init.bat

```bat
pip install -r requirements.txt

python -m nltk.downloader stopwords

pause
```

最後執行

```bash
python main.py
```
