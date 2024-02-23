import logging
import aiohttp
import requests
import parallel

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

def main():
    parallel.ParallelCompareWithUrl(urls, check_website_status, check_website_status_async).compare()

if __name__ == "__main__":
    main()

"""
반복 테스트 결과
      1(a->t->m)   2(a->t->m)   3(a->m->t)   4(t->a->m)   5(t->m->a)   6(m->a->t)   7(m->t->a)
asy         1.51         1.15         2.50         1.28         1.30         3.26         1.47
thr         5.74         5.80         5.77         6.23         5.74         6.03         5.91
mul         8.33         8.71         8.55         8.35         8.32         8.41         8.57

해석
http request의 경우는 aiohttp를 통해서 async 진행이 가능하다.
이에 따라 async가 가장 빠르다
멀티스레딩이 가장 느렸음.

"""