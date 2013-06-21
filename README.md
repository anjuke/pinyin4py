
[![Build Status](https://travis-ci.org/anjuke/pinyin4py.png)](https://travis-ci.org/anjuke/pinyin4py)

```
$ pip install pinyin4py
```

```python
from anjuke import pinyin

converter = pinyin.Converter()
converter.load_word_file('words.txt')
print converter.convert('中文测试')
```
