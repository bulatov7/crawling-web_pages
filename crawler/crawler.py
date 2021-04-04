import random
import re
import zipfile
 
import requests


def index_txt(links):
    f_index = open("index.txt", "w")
    pattern = "%d. %s\n"
    for i in range(len(links)):
        f_index.write(pattern % (i, host + links[i]))
    f_index.close()


def vykachka_zip(content):
    i = 0
    with zipfile.ZipFile('vykachka.zip', 'w') as f:
        for page in content:
            f.writestr("page" + str(i) + ".html", page)
            i += 1


def find_links(content):
    prefix = "/composition"
    links_regex = "href=[\"\']/composition(.*?)[\"\']"
    links = re.findall(links_regex, content)
    return list(
        map(lambda e: prefix + e, filter(lambda e: not str(e).endswith((".jpg", ".png", ".ogg")), links)))


def open_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        return None


if __name__ == '__main__':
    host = 'http://www.litra.ru'
    start_url = 'http://www.litra.ru/composition'
    start_page = open_url(start_url)
    links = find_links(start_page)
    links = links[:130]

    index_txt(links)
    links_content = []
    for link in links:
        content = open_url(host + link)
        if content is not None:
            links_content.append(content)

    vykachka_zip(links_content)
