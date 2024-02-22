import logging
import threading
import multiprocessing
import asyncio
import aiohttp
import asyncio
import requests
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO,
)

urls = [
    "github.com",
    "www.daum.net",
    "v.daum.net",
    "www.facebook.com",
    "www.google.com",
    "mail.google.com",
    "drive.google.com",
    "play.google.com",
    "aa.google.com",
    "apis.google.com",
    "accounts.google.com",
    "docs.python.org",
    "stackoverflow.com",
    "velog.io",
    "forums.docker.com",
    "aws.amazon.com",
    "amazon.com",
    "signin.aws.amazon.com",
    "codebeautify.org",
    "atlassian.net",
    "api.atlassian.com",
    "bitbucket.org",
    "ssl.gstatic.com",
    "fonts.gstatic.com",
    "www.gstatic.com",
    "xp.atlassian.com",
    "data.pendo.io",
    "www.bing.com",
    "th.bing.com",
    "assets.msn.com"
]

def check_website_status(url):
    try:
        response = requests.get("https://" + url)
        if response.status_code == 200:
            logging.debug(f"\t{url} :\t웹사이트 상태: 정상")
        else:
            logging.debug(f"\t{url} :\t웹사이트 상태: 비정상 ({response.status_code})")
    except Exception as err:
        logging.exception(f"\t{url} :\웹사이트 체크 에러 ({err})")
    
async def check_website_status_async(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://" + url) as response:
                if response.status == 200:
                    logging.debug(f"\t{url} :\t웹사이트 상태: 정상")
                else:
                    logging.debug(f"\t{url} :\t웹사이트 상태: 비정상 ({response.status})")
    except Exception as err:
        logging.exception(f"\t{url} :\웹사이트 체크 에러 ({err})")

def do_something(self, url):
    check_website_status(url)

async def do_something_async(self, url):
    await check_website_status_async(url)

def execute_by_threading():
    try:
        work_threads = []
        for url in urls:
            work_thread = threading.Thread(target=do_something, args=(1, url,))
            work_threads.append(work_thread)

        for work_thread in work_threads:
            work_thread.start()

        for work_thread in work_threads:
            work_thread.join()

        logging.debug("execute_by_threading done!")

    except Exception as err:
        logging.exception(f"execute_by_threading 에러 ({err})")

def execute_by_multiprocessing():
    try:
        processes = []
        for url in urls:
            p = multiprocessing.Process(target=do_something, args=(1, url,))
            processes.append(p)

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        logging.debug("execute_by_multiprocessing done!")

    except Exception as err:
        logging.exception(f"execute_by_multiprocessing 에러 ({err})")

async def execute_by_async():
    try:
        tasks = [do_something_async(1, url) for url in urls]
        await asyncio.gather(*tasks)

        logging.debug("execute_by_async done!");
    
    except Exception as err:
        logging.exception(f"execute_by_async 에러 ({err})")
        

def main():
    logging.info("--- Main Start ---")

    header_list_for_async = []
    elapsed_time_list_for_async = []
    elapsed_time_list_for_threading = []
    elapsed_time_list_for_multiprocessing = []

    logging.info("test 1 - order : async -> threading -> multiprocessing")
    header_list_for_async.append("1(a->t->m)")
    elapsed_time_list_for_async.append(execute_by_async_with_log());
    elapsed_time_list_for_threading.append(execute_by_threading_with_log());
    elapsed_time_list_for_multiprocessing.append(execute_by_multiprocessing_with_log());

    logging.info("test 2 - order : async -> threading -> multiprocessing")
    header_list_for_async.append("2(a->t->m)")
    elapsed_time_list_for_async.append(execute_by_async_with_log());
    elapsed_time_list_for_threading.append(execute_by_threading_with_log());
    elapsed_time_list_for_multiprocessing.append(execute_by_multiprocessing_with_log());

    logging.info("test 3 - order : async -> multiprocessing -> threading")
    header_list_for_async.append("3(a->m->t)")
    elapsed_time_list_for_async.append(execute_by_async_with_log());
    elapsed_time_list_for_multiprocessing.append(execute_by_multiprocessing_with_log());
    elapsed_time_list_for_threading.append(execute_by_threading_with_log());

    logging.info("test 4 - order : threading -> async -> multiprocessing")
    header_list_for_async.append("4(t->a->m)")
    elapsed_time_list_for_threading.append(execute_by_threading_with_log());
    elapsed_time_list_for_async.append(execute_by_async_with_log());
    elapsed_time_list_for_multiprocessing.append(execute_by_multiprocessing_with_log());

    logging.info("test 5 - order : threading -> multiprocessing -> async")
    header_list_for_async.append("5(t->m->a)")
    elapsed_time_list_for_threading.append(execute_by_threading_with_log());
    elapsed_time_list_for_multiprocessing.append(execute_by_multiprocessing_with_log());
    elapsed_time_list_for_async.append(execute_by_async_with_log());

    logging.info("test 6 - order : multiprocessing -> async -> threading")
    header_list_for_async.append("6(m->a->t)")
    elapsed_time_list_for_multiprocessing.append(execute_by_multiprocessing_with_log());
    elapsed_time_list_for_async.append(execute_by_async_with_log());
    elapsed_time_list_for_threading.append(execute_by_threading_with_log());

    logging.info("test 7 - order : multiprocessing -> threading -> async")
    header_list_for_async.append("7(m->t->a)")
    elapsed_time_list_for_multiprocessing.append(execute_by_multiprocessing_with_log());
    elapsed_time_list_for_threading.append(execute_by_threading_with_log());
    elapsed_time_list_for_async.append(execute_by_async_with_log());
    
    logging.info("    " + " ".join([f"{header:s}".rjust(12) for header in header_list_for_async]))
    logging.info("asy " + " ".join([f"{num:.2f}".rjust(12) for num in elapsed_time_list_for_async]))
    logging.info("thr " + " ".join([f"{num:.2f}".rjust(12) for num in elapsed_time_list_for_threading]))
    logging.info("mul " + " ".join([f"{num:.2f}".rjust(12) for num in elapsed_time_list_for_multiprocessing]))
    
    logging.info("--- Main End ---")

def execute_by_threading_with_log():
    start_time = time.time()
    execute_by_threading()
    return time.time() - start_time;

def execute_by_async_with_log():
    start_time = time.time()
    asyncio.run(execute_by_async())
    return time.time() - start_time;

def execute_by_multiprocessing_with_log():
    start_time = time.time()
    execute_by_multiprocessing()
    return time.time() - start_time;


if __name__ == "__main__":
    main()

"""
반복 테스트 결과
      1(a->t->m)   2(a->t->m)   3(a->m->t)   4(t->a->m)   5(t->m->a)   6(m->a->t)   7(m->t->a)
asy         1.66         1.32         1.31         1.44         1.27         1.48         1.19
thr         5.66         5.82         5.78         6.18         5.85         5.76         5.84
mul         8.87         8.69         8.98         8.90         8.64         8.72         8.88

해석
http request의 경우는 aiohttp를 통해서 async 진행이 가능하다.
이에 따라 async가 가장 빠르다
멀티스레딩이 가장 느렸음.

"""