import requests
from urllib.parse import urlparse
from linkfinder import LinkFinder
from general import create_project, file_to_set, set_to_file


class Spider:

    project_name = ''
    base_url = ''
    queue_file = ''
    crawled_file = ''
    htmls_file = ''
    queue_set = set()
    crawled_set = set()
    htmls_set = set()

    def __init__(self, project_name, base_url):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.queue_file = project_name + '/queue.txt'
        Spider.crawled_file = project_name + '/crawled.txt'
        Spider.htmls_file = project_name + '/htmls.txt'
        self.boot()
        self.crawled_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project(Spider.project_name, Spider.base_url)
        Spider.queue_set = file_to_set(Spider.queue_file)
        Spider.crawled_set = file_to_set(Spider.crawled_file)
        Spider.htmls_set = file_to_set(Spider.htmls_file)

    import requests
    
    @staticmethod
    def crawled_page(thread_name, page_url):
        if page_url not in Spider.crawled_set:
            print(f'{thread_name} crawling {page_url}')
            print(f'Queue {len(Spider.queue_set)}, crawled {len(Spider.crawled_set)}')
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue_set.remove(page_url)
            Spider.crawled_set.add(page_url)
            page = requests.get(page_url)
            Spider.htmls_set.add(page.content)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        print('gathering links from', page_url)
        responce = requests.get(page_url)
        # try из-за XML файлов
        try:
            if 'text/html' in responce.headers['content-type']:
                finder = LinkFinder(Spider.base_url, page_url)
                finder.feed(responce.text)
                return finder.get_links()
            else:
                return set()
        except:
            return set()


    @staticmethod
    def add_links_to_queue(links):
        if(len(Spider.crawled_set) <= 100):
            print(f'len(Spider.crawled_set) <= 100, {len(Spider.crawled_set) }')
            for url in links:
                if (url not in Spider.queue_set) and (url not in Spider.crawled_set):
                    if len(url.split('.')) > 1:
                        if Spider.in_domain(url, Spider.base_url):
                            Spider.queue_set.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue_set, Spider.queue_file)
        set_to_file(Spider.crawled_set, Spider.crawled_file)
        set_to_file(Spider.htmls_set, Spider.htmls_file)

    @staticmethod
    def in_domain(url, domain_name):
        if urlparse(url).netloc == urlparse(domain_name).netloc:
            return True
