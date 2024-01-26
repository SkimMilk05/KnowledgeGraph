import sys
sys.path.append('../')
from utils import ICD9CODES

import json

with open('finalwikidict.json', 'r') as f:
    finalwikidict = json.load(f)


print(f'{len(finalwikidict)} wiki pages found, {len(ICD9CODES)} ICD9 codes, {len(finalwikidict)/len(ICD9CODES)}')