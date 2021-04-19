import re
from urllib.parse import urlparse
import urllib.robotparser
"""
Implement the scraper function in scraper.py. 
The scraper function receives a URL and corresponding Web response 
(for example, the first one will be "http://www.ics.uci.edu" and the 
Web response will contain the page itself). Your task is to parse the 
Web response, extract enough information from the page (if it's a valid page) 
so to be able to answer the questions for the report, and finally, return 
the list of URLs "scrapped" from that page. 
Some important notes:
 - Make sure to return only URLs that are within the domains and paths 
   mentioned above! (see is_valid function in scraper.py -- you need to 
   change it) 
 - Make sure to defragment the URLs, i.e. remove the fragment part.
 - You can use whatever libraries make your life easier to parse things. 
   Optional dependencies you might want to look at: BeautifulSoup, lxml 
   (nudge, nudge, wink, wink!) 
 - Optionally, in the scraper function, you can also save the URL 
   and the web page on your local disk.
*************************************************************************
- Honor the politeness delay for each site
- Crawl all pages with high textual information content
- Detect and avoid infinite traps
- Detect and avoid sets of similar pages with no information
- Detect and avoid dead URLs that return a 200 status but 
  no data (click here to see what the different HTTP status 
  codes mean (Links to an external site.))
- Detect and avoid crawling very large files, especially if 
  they have low information value

"""
def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
   return list()

def is_valid(url):
    """
    returns true only if:
        *.ics.uci.edu/*
        *.cs.uci.edu/*
        *.informatics.uci.edu/*
        *.stat.uci.edu/*
        today.uci.edu/department/information_computer_sciences/*
    """
    try:
        parsed = urlparse(url) 
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        # checking robots.txt file for allowed URLS
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(parsed.scheme + '://' + parsed.netloc + "/robots.txt")
        rp.read()
        
        fileType = re.match(
            # finds groups that are not webpages
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        
        # returns true if URL valid and is a webpage
        return rp.can_fetch('*', url) and not fileType

    except TypeError:
        print ("TypeError for ", parsed)
        raise

if __name__ == "__main__":

    print(is_valid("https://docs.python.org/3/library/re.html"))
    