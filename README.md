# wallheaven_downer

wallheaven图片爬取，输入页面链接，最大的页数，以及要保存的文件夹路径即可

## 使用方法

#### 1.加cookie

有的页面不加cookie不能显示图片链接

wallheaven的cookie有效期蛮长的，所以就直接手动加了

![image-20220530213548748](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20220530213548748.png)

![image-20220530213954673](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20220530213954673.png)

#### 2.填写页面信息

![image-20220530213938379](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20220530213938379.png)

![image-20220530214223740](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20220530214223740.png)

#### 3.需要用到的库

```python
import math
import requests
import re
import aiohttp
import asyncio
import os.path
```

#### 4.程序介绍

1)使用协程快速爬取

2)异常检测，出现异常重新爬取

3)防重复，不会重复爬取同一张图片
