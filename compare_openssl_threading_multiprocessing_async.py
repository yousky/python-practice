import logging
import threading
import multiprocessing
import asyncio
import ssl
import OpenSSL
from datetime import datetime, UTC
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO,
)

urls = [
    "github.com",
    "www.daum.net",
    "v.daum.net",
    "mail.daum.net",
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

def check_cert_expiry(url):
    try:
        cert = ssl.get_server_certificate((url, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        expiry_date = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        days_to_expiry = (expiry_date - datetime.now(UTC).replace(tzinfo=None)).days
        logging.debug(f"\t{url} :\tSSL 인증서 만료까지 남은 기간: {days_to_expiry}일")
    except Exception as err:
        logging.exception(f"\t{url} :\t인증서 체크 에러 ({err})")


def do_something(self, url):
    check_cert_expiry(url)

async def do_something_async(self, url):
    check_cert_expiry(url)

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
asy         5.29         3.68         3.73         3.89         3.66         3.67         3.86
thr         0.60         0.64         0.62         0.59         0.61         0.69         0.59
mul         2.14         2.07         1.96         2.02         1.95         2.06         1.86

해석
인증서 check의 경우는 별다른 async관련 함수가 없어서 
threading을 통해서 동시에 여러개 실행 하는 것이 가장 빠르다
async가 가장 느렸다. 어딘가 딜레이 되는 곳이 있는 듯.. 

"""