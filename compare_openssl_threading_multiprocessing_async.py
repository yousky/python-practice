import logging
import ssl
import OpenSSL
from datetime import datetime, UTC
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

def check_cert_expiry(url):
    try:
        cert = ssl.get_server_certificate((url, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        expiry_date = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        days_to_expiry = (expiry_date - datetime.now(UTC).replace(tzinfo=None)).days
        logging.debug(f"\t{url} :\tSSL 인증서 만료까지 남은 기간: {days_to_expiry}일")
    except Exception as err:
        logging.exception(f"\t{url} :\t인증서 체크 에러 ({err})")

async def check_cert_expiry_async(url):
    check_cert_expiry(url)

def main():
    parallel.ParallelCompareWithUrl(urls, check_cert_expiry, check_cert_expiry_async).compare()

if __name__ == "__main__":
    main()

"""
first synchronous for execution time :4.64
last synchronous for execution time :4.07
반복 테스트 결과
      1(a->t->m)   2(a->t->m)   3(a->m->t)   4(t->a->m)   5(t->m->a)   6(m->a->t)   7(m->t->a)
asy         4.11         3.91         3.99         4.11         4.16         4.14         4.25
thr         0.62         0.64         0.59         0.62         0.62         0.62         0.60
mul         2.05         2.05         2.01         2.41         2.05         2.03         2.05

해석
인증서 check의 경우는 별다른 async관련 함수가 없어서 
threading을 통해서 동시에 여러개 실행 하는 것이 가장 빠르다
async가 가장 느렸다. 어딘가 딜레이 되는 곳이 있는 듯.. synchronous와 큰 차이가 없음.

"""