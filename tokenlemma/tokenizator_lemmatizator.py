import re
import string
import zipfile

import nltk
import pymorphy2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()


def read_file(zip_file, f):
    html = zip_file.open(f)
    return html


# def get_tokenizator_cond():
#     stop_words = stopwords.words('russian')
#     return lambda word: word not in stop_words


def set_tokenizator_res(result):
    index_html = open("tokenizator.txt", "a")
    pattern = "%s\n"
    for word in result:
        index_html.write(pattern % word)
    index_html.close()


def tokenizator(html):
    page_content = BeautifulSoup(html).get_text()
    # tokenizator_cond = get_tokenizator_cond()
    result = list(nltk.wordpunct_tokenize(page_content))
    result = minus_znak_prep(result)
    result = list(filter(minus_incorrect_sym, result))
    return result


def minus_znak_prep(values):
    return [i for i in values if all(not j in string.punctuation for j in i)]


def minus_incorrect_sym(word):
    rus = re.compile(r'^[а-яА-Я]{2,}$')
    numbers = re.compile(r'^[0-9]+$')
    res = bool(rus.match(word)) or bool(numbers.match(word))
    return res


def get_lemma(word):
    p = morph.parse(word)[0]
    if p.normalized.is_known:
        normal_form = p.normal_form
    else:
        normal_form = word.lower()
    return normal_form


def lemmatizator(tokenizator_res):
    lemmatizator_arr = dict()
    for word in tokenizator_res:
        normal_form = get_lemma(word)
        if not normal_form in lemmatizator_arr:
            lemmatizator_arr[normal_form] = []
        lemmatizator_arr[normal_form].append(word)
    return lemmatizator_arr


def set_lemmatizator_res(lemmatizator_res):
    f_lemma = open("lemmatizator.txt", "a")
    for lemma, tokens in lemmatizator_res.items():
        f_words = lemma + " "
        for token in tokens:
            f_words += token + " "
        f_words += "\n"
        f_lemma.write(f_words)
    f_lemma.close()


if __name__ == '__main__':
    nltk.download('stopwords')
    zip = zipfile.ZipFile('vykachka.zip', 'r')
    tokenizator_res = set()
    for f in zip.filelist:
        page_html = read_file(zip, f.filename)
        token_file = set(tokenizator(page_html))
        tokenizator_res = tokenizator_res | token_file
        print("tokenization for", f.filename, "finished")
    set_tokenizator_res(tokenizator_res)
    lemmatizator_res = lemmatizator(tokenizator_res)
    set_lemmatizator_res(lemmatizator_res)
