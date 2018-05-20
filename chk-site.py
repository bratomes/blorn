# import modules
import urllib2
import urlparse
import glob
import bs4

# global variables
LOG_FILE = "teste.log"
BODY_KEYWORDS = []
META_KEYWORDS = []


def scan_log(file):
    global user
    squid_log = open(file, 'r')

    if glob.glob('domain.log'):
        for line in squid_log.readlines():
            line = line.split()
            user = line[7]
            status_code = line[3][-3:]

            domain = urlparse.urlsplit(line[6])[1]

            # check if squid is authenticated through the status code in log file
            if status_code != '407':
                # put the domain in a log file to not check that again
                if not check_file(domain, 'domain.log') and '.' in domain:
                    domain_log = open('domain.log', 'a+')
                    domain_log.write(domain + '\n')
                    domain_log.close()
                    check_website(domain)

    squid_log.close()


def check_file(domain, logfile):
    if domain in open(logfile).read():
        return True
    else:
        return False


def check_website(domain):
    url = urllib2.urlopen('http://' + domain, timeout=10)

    if url:
        data = url.read()
        soup = bs4.BeautifulSoup(data)
        meta_tags = soup.find('meta', {'name': 'keywords'})['content'].split(',')

    if meta_tags:
        for tag in meta_tags:
            if tag in META_KEYWORDS:
                porn_log = open('porn.log', 'a')
                porn_log.write(domain + ' -> ' + tag + ' -> ' + user[7] + '\n')
                porn_log.close()
                return False
    else:
        for keyword in BODY_KEYWORDS:
            if keyword in data:
                porn_log = open('porn.log', 'a')
                porn_log.write(domain + ' -> ' + tag + ' -> ' + user[7] + '\n')
                porn_log.close()
                return False


scan_log(LOG_FILE)
