import re
import aiohttp
import asyncio
import os.path

# 填写页面链接，注意去掉page参数
originUrl = ''
# 要爬取页面的最大页数
max_page = 1
# 图片保存的路径
path = ''

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
    'cookie': ''
}

# 正则表达式
com = re.compile('<a class="preview" href="(?P<url>.*?)"  target="_blank"', re.S)

urls = []
photo_urls = []
photo_names = []
# 信号量，控制协程数，防止爬的过快
sem = asyncio.Semaphore(10)
new_photo_count = 0
old_photo_count = 0


def confirm_param():
    global originUrl
    if len(originUrl) > 30:
        originUrl += '&page='
    else:
        originUrl += '?page='


async def get_urls(url, page_num, session):
    print("开始获取第" + str(page_num) + "页的图片链接")
    while True:
        async with sem:
            await asyncio.sleep(1.5)
            print('发出请求' + str(page_num) + 'url:' + url)
            try:
                async with await session.request('GET', url, headers=headers) as resp:  # 提出请求
                    print(resp.status)
                    if resp.status == 200:
                        page_content = await resp.text()
                        break
            except:
                print('url:' + url + "请求被拒绝")
    # print(page_content)
    # 迭代器
    the_iter = com.finditer(page_content)
    for it in the_iter:
        # print(it.group("url"))
        urls.append(it.group("url"))


def get_photo_url_by_name(url_array):
    for url in url_array:
        photo_name = url.split('/')[-1]
        pre_name = photo_name[:2]
        url = f"https://w.wallhaven.cc/full/{pre_name}/wallhaven-{photo_name}.jpg"
        photo_urls.append(url)
        print(url)
        photo_name += '.jpg'
        photo_names.append(photo_name)


async def save_a_photo(photo_url, index, session):
    # print('原url'+photo_url)
    while True:
        async with sem:
            jpg_photo_name = str(photo_names[index][:-3]) + 'jpg'
            jpg_path = path + jpg_photo_name
            png_photo_name = str(photo_names[index][:-3]) + 'png'
            png_path = path + png_photo_name
            if not os.path.exists(jpg_path) and not os.path.exists(png_path):
                try:
                    async with await session.request('GET', photo_url, headers=headers) as resp:
                        if resp.status == 429:
                            print("429请求过快")
                            continue
                        print(resp.status)
                        if resp.status == 404:
                            photo_names[index] = str(photo_names[index][:-3]) + 'png'
                            photo_url = photo_url[:-3] + 'png'
                            print('修正后的url为:' + photo_url)
                            try:
                                async with await session.request('GET', photo_url, headers=headers) as resp2:
                                    photo_content = await resp2.read()
                                    if resp2.status == 200:
                                        with open(path + photo_names[index], mode='wb')as f:
                                            f.write(photo_content)
                                            print(str(index) + ":" + str(photo_names[index]) + '保存成功')

                                        break
                            except:
                                print('图片保存失败:' + photo_url)
                        else:
                            photo_names[index] = str(photo_names[index][:-3]) + 'jpg'
                            photo_content = await resp.read()
                            if resp.status == 200:
                                with open(path + photo_names[index], mode='wb')as f:
                                    f.write(photo_content)
                                    print(str(index) + ":" + str(photo_names[index]) + '保存成功')
                                break
                except:
                    print('图片保存失败:' + photo_url)
            else:
                print("图片" + photo_names[index][:-4] + "已存在")
                break


async def main_save_photo(photo_url_array):
    tasks = []
    index = 0
    async with aiohttp.ClientSession() as session:
        for url in photo_url_array:
            tasks.append(asyncio.create_task(save_a_photo(url, index, session)))
            index += 1
        await asyncio.wait(tasks)


async def main_get_urls(page_num):
    tasks = []  # 把所有任务放到一个列表中
    async with aiohttp.ClientSession() as session:  # 获取session
        for index in range(1, page_num + 1):
            tasks.append(asyncio.create_task(get_urls(originUrl + str(index), index, session)))
        print(len(tasks))
        await asyncio.wait(tasks)  # 激活协程


if __name__ == '__main__':
    confirm_param()
    print(max_page)
    loop = asyncio.get_event_loop()  # 获取事件循环
    loop.run_until_complete(main_get_urls(max_page))  # 激活协程
    print(urls)
    print(len(urls))
    get_photo_url_by_name(urls)
    loop = asyncio.get_event_loop()  # 获取事件循环
    loop.run_until_complete(main_save_photo(photo_urls))  # 激活协程
