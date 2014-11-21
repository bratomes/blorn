# import modules
import urllib2
import urlparse
import glob
import bs4

# global variables
LOG_FILE = "teste.log"
BODY_KEYWORDS = ('acompanhantes em belem','garotas de programa','zoofilia',
'blowjob','fucking ass','sex with animals','sexo com animais','sex videos','porn movies',
'big dick','big cock','cam porn','big tits','cumshot','videos eroticos','boquetes','boquete',
'boquetes','hentai','punheta','ass lick','brunette','black cock','creampie','videos porno',
'depravadas','So Gostosas HP','youvideos','zoo porn','horse porn','animal porn','bestiality porn',
'videos de sexo','horse fuck','porn videos','pets porn','dog fuck','animal sex movies',
'animal porn tube','filmes de sexo','free porn')
META_KEYWORDS = ('sexo','sex','fuck','xxx','pussy','cum','anal','creampie','tits','nude','cumshot',
'animal sex','porn','porno','zoo sex','sexo animal','piroca','dick','buceta','porntube','xvideos',
'youvideos')

# scan log file 
def scan_log(file):
    global user
    
    # open squid log
    squid_log = open(file, 'r')

    if glob.glob('domain.log'):
        for line in squid_log.readlines():
    	    line = line.split()
    	    status_code = line[3][-3:]
    	    user = line[7]
    	    domain = urlparse.urlsplit(line[6])[1]
    
            # check if squid is authenticated through the status code in log file
            if status_code != '407':
                # put the domain in a log file to not check that again
                if check_file(domain, 'domain.log') == False and '.' in domain:
                    domain_log = open('domain.log', 'a+')
                    domain_log.write(domain + '\n')
                    domain_log.close()
                    check_website(domain)  
    else:
	    domain_log_file = open('domain.log', 'w')
	    scan_log(LOG_FILE)

    squid_log.close()

# check if there is a domain in some log file
def check_file(domain, logfile):
    if domain in open(logfile).read():
        return True
    else:
        return False

def check_website(domain):
    try:
        url = urllib2.urlopen('http://' + domain, timeout = 10)
    
        if url:
            data = url.read()
            soup = bs4.BeautifulSoup(data)
            meta_tags = soup.find('meta', {'name':'keywords'})['content'].split(',')
            
        if meta_tags:
            for tag in meta_tags:
                if tag in META_KEYWORDS:
                    print tag
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

    except:
        pass
    

scan_log(LOG_FILE)