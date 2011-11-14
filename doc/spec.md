# 汉字转拼音 (hz2py)

我们希望安居客的搜索引擎能够更好的做到同音字的容错，采用拼音容错是一个不错的方法。因此，需要一个将汉字转换为拼音的组件。同时，汉字转拼音组件还可以有多个用途，例如以拼音的首字母来检索小区名、人名等。

这样我们需要一个通用的将汉字转换为拼音的服务。

## 功能
基本功能就是中文拉丁化，输入一段中文文本，输出转变为汉语拼音的文本。

要求原文中的全角标点符号、空格等应该转为对应的半脚符号。原汉字与英文间如果没有空格分隔，转换为拼音后应该加入空格分隔。

例如，“**我的英文名是Bob。**” 转化后为'**wo de ying wen ming shi Bob.**'

### 多种输出格式

* 声调
    `wǒ dē yīng wén míng shì Bob`或`wo3 de1 ying1 wen2 ming2 shi4 Bob`

* 声母输出
    `w d y w m sh Bob`

* 首字母输出
    `w d y w m s Bob`

### 词组形式的拼音输出
允许将一个中文词组以拼音词组的形式输出。本服务不需考虑中文分词，要求输入的文本已经是分词完毕的。

例如输入

    南京市 长江 大桥
    
输出：
    
    nanjingshi changjiang daqiao

注意与缺省情况下一个汉字一个拼音分隔的输出格式的区别。

### 多音字处理
应该能够智能的处理多音字的情况，例如
输入：

    南京市长江大桥

输出：

    nan jing shi chang jiang da qiao

在无法智能辨认多音字的情况下，同时输出一个字或词的多个拼音，以|符号分隔多音字(词)。

例如：输入：

    南京市长江大桥

输出：

    nan jing shi chang|zhang jiang da|dai qiao

以词组为切分单位时，输出整个词的多种拼音

输入：

    南京市 长江 大桥
    
输出：
    
    nanjingshi changjiang|zhangjiang daqiao|daiqiao

需要建立合理的拼音词库以解决常用的多音字问题，例如“莘庄立交”、“北翟路”等

### 南方口音
不再区分前后鼻音、卷舌音、翘色音，例如

    wo de yin wen min si Bob

对应表为：

    z = zh              c = ch              s = sh
    k = g               f = h               l = n
    an = ang            en = eng            in = ing
    lan = lang          uan = uang          l = r


## API

服务名称：**hz2py**

### convert(text, fmt=[df], sc=True, pp=False, fuzzy=0) ###

#### 参数 ####

* **text**
    待转换的中文文本

* **fmt**
    设定转换的方式的格式。缺省为返回单字拆分的拼音格式

    * `df` - Default 全拼
    * `tm` - Tone Marks 全拼带音调
    * `tn` - Tone Numbers 全拼带数字形式的音调
    * `ic` - Initial Consonant only 声母
    * `fl` - First Letter 首字母

* **sc**
    Split Character，是否以单个汉字为切割单位的拼音输出字为单位
    * `True` - 单字拆分
    * `False` - 不拆分。以输入的中文文本的分词为准

* **pp**
    Polyphone 是否输出无法判断的多音字(词)
    * `False` - 不输出多音字
    * `True` - 输出多音字

* **fuzzy**
    Puzzy 拼音模糊化
    * `0` - 不处理
    * `1` - 模糊化 z-zh c-ch s-sh
    * `2` - 模糊化 k-g f-h l-n l-r
    * `4` - 模糊化 an-ang en-eng in-ing lan-lang uan-uang

#### 返回结果 ####
如果只需要一个格式，直接返回转换后的结果。例如调用`convert('南京市长江大桥')` 返回：

```
nan jing shi chang jiang da qiao
```
如果有多个格式选项，返回所有格式的结果。例如调用`convert('南京市 长江 大桥', fmt=[tm,tn,fl], sc=False)` 返回：

```
{
    'tm': 'nánjīngshì chángjīang dàqiáo'
    'tn': 'nan2jing1shi4 chang2jiang1 da4qiao2'
    'fl': 'njs cj dq'
}
```

假设转拼音服务无法识别“莘”字在下面短语中的读音，当调用`convert('莘庄 立交', fmt=[tn,fl], sc=False, pp=True)`将返回：

```
{
    'tn': 'xin1zhuang1|shen1zhuang1 li4jiao3'
    'fl': 'xz|sz lj'
}
```
