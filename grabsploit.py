import argparse
import json
import os
import pandas as pd
import random
import requests
from config import headers


class Exploit:
    def __init__(self, args):
        if args.auth:
            if os.path.exists('config/.api_key'):
                exit("Active authentication detected. If you want to re-authenticate with another api key, delete/edit the current .apikey.auth file")
            else:
                with open('config/.api_key', 'w') as file:
                    self.api_key = args.auth
                    file.write(self.api_key)
                    file.close()
                exit("api key is Successfully saved to the .apikey.auth file")
        else:
            with open('config/.api_key', 'r') as file:
                self.api_key = file.readline().strip()

        self.url = 'https://api.criminalip.io/v1/exploit/search'
        self.headers = {
            "x-api-key": self.api_key,
            "User-Agent": random.choice(headers.user_agents)
        }

        if args.query:
            self.exploit_query()
        elif args.cve_id:
            self.exploit_query(cve_id=args.cve_id)
        elif args.edb_id:
            self.exploit_query(edb_id=args.edb_id)
        elif args.platform:
            self.exploit_query(platform=args.platform)

        if args.read:
            self.read_csv_file(args.read)

    def exploit_query(self, offset=None, cve_id=None, edb_id=None, title=None, platform=None):
        params = {
            'query': '"{}"'.format(args.query),
            'offset': 0,
        }

        if args.start:
            params['offset'] = args.start

        if cve_id:
            params['query'] = 'cve_id: {}'.format(cve_id)
        elif edb_id:
            params['query'] = 'edb_id: {}'.format(edb_id)
        elif platform:
            params['query'] = 'platform: {}'.format(platform)

        res = requests.get(url=self.url, params=params, headers=self.headers)
        res = res.json()

        edb_list = []
        if res['status'] == 200:
            for r in res['data']['result']:
                edb_data = [r['edb_id'], r['author'], r['title'], r['platform'], r['type'], r['edb_reg_date'], 'edb_contents/{}'.format(r['edb_id'])]
                edb_list.append(edb_data)

                with open('edb_contents/{}'.format(r['edb_id']), 'w') as file:
                    file.write("{}".format(r['edb_content']))
                    file.close()

        df = pd.DataFrame(
            data = edb_list,
            columns = ['edb_id', 'author', 'title', 'platform', 'edb_type', 'edb_reg_date', 'edb_content']
        )
        print(df)

        if args.download:
            if not args.start:
                args.start = 0
            file_name = "{}_{}.csv".format(args.download, args.start)
            df.to_csv(file_name, index=False, sep='\t')

    def read_csv_file(self, csv_file_path):
        df = pd.read_csv(csv_file_path, sep='\t')
        print(df.to_string())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Zvan by criminalip')
    parser.add_argument('-A', '--auth', help='api authentication with a valid criminalip.io api key', metavar='<api_key>')
    parser.add_argument('-Q', '--query', help='Return exploit data from query', metavar='<exploit_query>')
    parser.add_argument('-D', '--download', help='CSV download result of the exploit search', metavar='<file_path>')
    parser.add_argument('-R', '--read', help='Read the exploit search result CSV file', metavar='<file_path>')
    parser.add_argument('-C', '--cve-id', help='Exploit search with CVE_ID', metavar='<cve_id>')
    parser.add_argument('-E', '--edb-id', help='Exploit search with EDB_ID', metavar='<edb_id>')
    parser.add_argument('-P', '--platform', help='Exploit search with platform', metavar='<platform>')
    parser.add_argument('-S', '--start', help='start offset', metavar='<start_num>')

    args = parser.parse_args()

    exploit = Exploit(args)
