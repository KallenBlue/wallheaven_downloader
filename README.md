# wallheaven_downloader

wallheaven图片爬取，输入页面链接，最大的页数，以及要保存的文件夹路径即可

## 使用方法

#### 1.加cookie

有的页面不加cookie不能显示图片链接

wallheaven的cookie有效期蛮长的，所以就直接手动加了
![image-20220530213548748](https://user-images.githubusercontent.com/79305507/171006163-ada17108-093a-4503-bf6d-409a894dbb09.png)
![image-20220530213954673](https://user-images.githubusercontent.com/79305507/171006206-9de587d3-fd52-41c4-957d-5d24f00434c7.png)


#### 2.填写页面信息
![image-20220530213938379](https://user-images.githubusercontent.com/79305507/171006261-bdb00f5e-ac88-4899-b139-4bfdc894710f.png)
![image-20220530214223740](https://user-images.githubusercontent.com/79305507/171006289-18b5c1f2-9e8c-44ba-8d1f-1e57b70c7e10.png)

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
