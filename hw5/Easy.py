import asyncio
import aiohttp
import aiofiles
import time
import sys
from functools import wraps


def async_measure_time(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        finish = time.perf_counter()
        print(f"Executed {func.__name__} in {finish - start} sec")
        return result
    return wrap


async def download_one_picture(url, session, num):
    async with session.get(url) as response:
        f = await aiofiles.open(f"artifacts/pic{num}.jpg", mode='wb')
        await f.write(await response.read())
        await f.close()


@async_measure_time
async def download_pictures(url, num_pictures):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_pictures):
            task = asyncio.create_task(download_one_picture(url, session, i + 1))
            tasks.append(task)
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            print(repr(e))


def easy_run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_pictures("https://picsum.photos/200", int(sys.argv[1])))