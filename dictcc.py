#!/usr/bin/python3

import sys
import requests
import argparse
import os
import textwrap

from tabulate import tabulate
from bs4 import BeautifulSoup

_, columns = os.popen('stty size', 'r').read().split()


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
    str_tag = " ".join([a_tag.text for a_tag in tag.find_all('a')])
    if tag.dfn:
        all_dfn = ", ".join([dfn_tag.text for dfn_tag in tag.find_all('dfn')])
        str_tag = ' '.join([str_tag, '(' + all_dfn + ')'])

    return '\n   '.join(textwrap.wrap(str_tag, (int(columns) - 8) / 2))


# TODO: lookup response handling
def parse_response(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = [tag for tag in soup.find_all('td', 'td7nl')]

    raw_from_to = zip(data[::2], data[1::2])
    res_from_to = list()

    for f, t in raw_from_to:
        res_from_to.append([parse_single_tag(f), parse_single_tag(t)])

    return res_from_to


def parse_suggestions(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = [tag.a.text for tag in soup.find_all('td', 'td3nl') if tag.a]

    return data


def main(args):
    # prepend space to word
    words = ' '.join(args.word)
    # consult dict.cc website
    c = request(words, args.prim, args.sec)
    # response handling
    data = parse_response(c)

    if data:
        # print table if response was good
        print(tabulate(data, [args.prim, args.sec], tablefmt='orgtbl'))
    else:
        # suggestions if response was bad
        print(' '.join(["No translation found for:", words]))
        # handle suggestion response
        suggestions = parse_suggestions(c)
        print('\nHere are suggestions given by dict.cc:')
        for s in suggestions:
            print(" - {}".format(s))

    return 0


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
    parser.add_argument('-p', '--prim', type=str, default='en', help='Primary language')  # -p for setting primary language
    parser.add_argument('-s', '--sec', type=str, default='de', help='Secondary language')  # -s for setting secondary language
    parser.add_argument('word', help='word to translate', nargs='+')  # word to translate is last argument

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
