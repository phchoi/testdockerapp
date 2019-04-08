#!/usr/bin/env python

import argparse
import json
import requests

class Lookup(object):
    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--title', type=str, action='store',
                            default='Guardians of the Galaxy Vol. 2',
                            help="Provide title of the movie to lookup from omdb")
        parser.add_argument('-u', '--url', type=str, action='store',
                            default='http://127.0.0.1:38000/movie',
                            help="The URL of the API endpoint")

        args = parser.parse_args()

        endpoint = args.url
        if args.title:
            title = args.title
            search_string = {'title': title }

        #if not args['title']:
        response = requests.get(endpoint, params=search_string)

        data =  json.loads(response.text)

        print(data['message'])
