#!/usr/bin/python3

import argparse
import os
import textwrap

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# request number of "rows and columns" for command line (?) from kernel
# in PyCharm enable "emulate terminal in output console" in the run configuration for app
_, columns = os.popen('stty size', 'r').read().split()

requests_session = requests.Session()


def request(word, f, t):
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
    payload = {'s': word}

    try:
        # contact server
        r = requests.get(
            "https://{}{}.dict.cc/".format(f, t),
            headers=header,
            params=payload)
    except Exception as exception:
        print(exception)
        exit(1)

    return r.content


def parse_single_tag(tag):
    # prepend text content in a_tag that are HTML anchor elements
    str_tag = " ".join([a_tag.text for a_tag in tag.find_all('a')])
    # handling HTML (marked) definitions
    if tag.dfn:
        # prepend comma space if tag.dfn is a definition HTML element
        all_dfn = ", ".join([dfn_tag.text for dfn_tag in tag.find_all('dfn')])
        # put all definitions in brackets
        str_tag = ' '.join([str_tag, '(' + all_dfn + ')'])
    # wraps dict.cc results into multiple lines
    return '\n   '.join(textwrap.wrap(str_tag, (int(columns) - 8) / 2))  # TODO: look into this more


def parse_response(html):
    # standard html parser from bs4
    soup = BeautifulSoup(html, 'html.parser')
    # extracts tag into list
    data = [tag for tag in soup.find_all('td', 'td7nl')]  # TODO: look into this more
    # use iterable to get data content
    raw_from_to = zip(data[::2], data[1::2])
    # create new list
    res_from_to = list()

    for f, t in raw_from_to:
        # collect results
        res_from_to.append([parse_single_tag(f), parse_single_tag(t)])

    return res_from_to


def parse_suggestions(html):
    # standard html parser from bs4
    soup = BeautifulSoup(html, 'html.parser')
    # extract suggestions
    data = [tag.a.text for tag in soup.find_all('td', 'td3nl') if tag.a]  # TODO: look into this more

    return data


def handle_translation(word, primary_lang, secondary_lang):
    c = request(word, primary_lang, secondary_lang)
    data = parse_response(c)

    if data:
        print(tabulate(data, [primary_lang, secondary_lang], tablefmt='orgtbl'))
    else:
        print(' '.join(["No translation found for:", word]))
        suggestions = parse_suggestions(c)
        print('\nHere are suggestions given by dict.cc:')
        for s in suggestions:
            print(" - {}".format(s))


def main(args):
    if not args.console and args.word:
        handle_translation(args.word[0], args.prim, args.sec)
    elif args.console:
        print('Starting console')
        print('Enter your words for translation')
        print('Enter q for exit')

        user_input = input('>> ')
        while user_input != 'q':
            handle_translation(user_input, args.prim, args.sec)
            user_input = input('>> ')


if __name__ == '__main__':
    # primary dictionaries as a list of strings
    prim = ['de', 'en']
    # secondary dictionaries as a list of strings
    sec = ['bg', 'bs', 'cs', 'da', 'el', 'eo', 'es', 'fi', 'fr', 'hr',
           'hu', 'is', 'it', 'la', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sk',
           'sq', 'sr', 'sv', 'tr']
    # all dict list
    all_dict = prim + sec
    # handle command line arguments
    parser = argparse.ArgumentParser(
        description='Query dict.cc for a translation.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--prim', type=str, default='en', help='Primary language')
    parser.add_argument('-s', '--sec', type=str, default='de', help='Secondary language')
    parser.add_argument('-c', '--console', action='store_true')
    parser.add_argument('word', nargs=argparse.REMAINDER, help='word to translate')

    args = parser.parse_args()  # parse arguments using python function

    # handling user error
    if args.prim not in prim:
        print("Primary lang must be in : [" + ", ".join(prim) + "]")
        exit(1)
    if args.sec not in all_dict:
        print("Secondary lang must be in : [" + ", ".join(all_dict) + "]")
        exit(1)
    if args.prim == args.sec:
        print("Given languages must be different. Given : \"{}\" and \"{}\"".format(args.prim, args.sec))
        exit(1)

    main(args)  # conditional statement can't be moved to top because of this line
