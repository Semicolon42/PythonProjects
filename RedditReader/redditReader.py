import logging
import csv
import time
from bs4 import BeautifulSoup
import requests



logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls

    def download_url(self, url):
        response = None
        for x in range(1,5):
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response is not None and response.status_code == 200:
                break
        return response

    def get_reddit_posts(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        attrs = {'data-click-id': 'body'}

        rposts = []
        for post in soup.find_all('a', attrs=attrs):
            post_url = 'https://www.reddit.com'+post.attrs['href']
            post_text = self.get_reddit_post_text(post_url)
            rposts.append((post_url, post.h3.text, post_text))

        return rposts

    def get_reddit_post_text(self, url):
        response = self.download_url(url)
        print(response.status_code, url)

        soup = BeautifulSoup(response.text, 'html.parser')
        temp = soup.find('div', attrs={'data-test-id': 'post-content'})
        post_content = "NOT FOUND"
        if temp is not None:
            for div in temp.descendants:
                if hasattr(div, 'attrs') and 'data-click-id' in div.attrs:
                    try:
                        for p in div.find_all('p'):
                            post_content = post_content + " " + p.text
                    except Exception:
                        logging.exception(f'Failed to get post content: {url}')
        
        return post_content

    def crawl(self, url):
        response = self.download_url(url)
        html = response.text
        print("starting the crawl...")
        posts = self.get_reddit_posts(url, html)
        for rpost in posts:
            print(f'/////////////////////////////////////')
            print(rpost)
            print(f'/////////////////////////////////////')

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)



def main():
    Crawler(urls=['https://www.reddit.com/r/BoardGameExchange/new/']).run()

if __name__ == '__main__':
    print('start up')
    main()
    print('all done')
    