# Imports
import queue
import requests
import threading
import sys


AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
EXTENSIONS = [".php", ".back", "orig", ".inc", ".bk", "htm"]
THREADS = 50


def get_words(wordlist, resume=None):

    def extend_words(word):
        if "." in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')
        
        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')

    with open(wordlist) as f:
        raw_words = f.read()
    
    found_resume = False
    words = queue.Queue()

    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming Wordlist from: {resume}')
        else:
            print(word)
            extend_words(word=word)
    
    return words


def dir_brute(target, words):
    headers = {'User-Agent': AGENT}

    while not words.empty():
        url = f"{target}{words.get()}"

        try:
            r = requests.get(url=url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x')
            sys.stderr.flush()
            continue

        if r.status_code == 200:
            print(f"\nSuccess ({r.status_code}: {url})")
        elif r.status_code == 404:
            sys.stderr.write('.')
            sys.stderr.flush()
        else:
            print(f'{r.status_code} => {url}')


if __name__ == "__main__":
    target = input("Enter Target URL: ")
    wordlist = input("Enter Wordlist path: ")

    words = get_words(wordlist=wordlist)

    print('Press return to continue')

    sys.stdin.readline()

    for _ in range(THREADS):
        t = threading.Thread(target=dir_brute, args=(target, words, ))
        t.start()
 

