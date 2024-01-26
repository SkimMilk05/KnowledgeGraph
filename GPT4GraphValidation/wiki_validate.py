'''
    This script validates the knowledge graph created using GPT4 by seeing if
    the concepts are mentioned in the wikipedia page
    (We are essentially checking to make sure GPT4 did not "make up" false information)
'''

import json
import sys
sys.path.append('../')
from utils import ICD9CODES

with open('GPT4_sosy_knowgraph.json', 'r') as f:
    sosy_knowgraph = json.load(f)

with open('GPT4_treat_knowgraph.json', 'r') as f:
    treat_knowgraph = json.load(f)

with open('wiki_sosy_sets.json', 'r') as f:
    sosy_sets = json.load(f)

with open('wiki_treat_sets.json', 'r') as f:
    treat_sets = json.load(f)

TP1 = 0
FP1 = 0
print('len sosy before val', len(sosy_knowgraph.keys()))
sosy_knowgraph_wikival = dict()
for icd, list_concepts in sosy_knowgraph.items():
    try:
        setS = sosy_sets[icd]
        adjlist = []
        for concept in list_concepts:
            if concept in setS:
                TP1 += 1
                adjlist.append(concept)
            else:
                FP1 += 1
                # print(f'{concept} not in setS for {icd}!')
        sosy_knowgraph_wikival[icd] = adjlist
    except KeyError:
        # print(f'Manual backup method - KeyError for {icd}')
        sosy_knowgraph_wikival[icd] = []
print('len sosy after val', len(sosy_knowgraph_wikival.keys()))
sosy_precision = TP1/(TP1+FP1)
print(f'--------> SOSY - TP: {TP1}, FP: {FP1}, Precision: {sosy_precision}')


TP2 = 0
FP2 = 0
print('len treat before val', len(treat_knowgraph.keys()))
treat_knowgraph_wikival = dict()
for icd, list_concepts in treat_knowgraph.items():
    try:
        setS = treat_sets[icd]
        adjlist = []
        for concept in list_concepts:
            if concept in setS:
                TP2 += 1
                adjlist.append(concept)
            else:
                FP2 += 1
                # print(f'{concept} not in setS for {icd}!')
        treat_knowgraph_wikival[icd] = adjlist
    except KeyError:
        # print(f'Manual backup method - KeyError for {icd}')
        treat_knowgraph_wikival[icd] = []
print('len treat before val', len(treat_knowgraph_wikival.keys()))
treat_precision = TP2/(TP2+FP2)
print(f'--------> TREATMENT - TP: {TP2}, FP: {FP2}, Precision: {treat_precision}')

TP = TP1+TP2
FP = FP1+FP2
precision = TP/(TP+FP)
print(f'--------> OVERALL - TP: {TP}, FP: {FP}, Precision: {precision}')
# for k, v in treat_knowgraph_wikival.items():
#     if k not in sosy_knowgraph_wikival.keys():
#         print('This k, v is in treat but not sosy')
#         print(k, v)
#         sosy_knowgraph_wikival[k] = []

for code in ICD9CODES:
    if code not in sosy_knowgraph_wikival.keys():
        sosy_knowgraph_wikival[code] = []
    if code not in treat_knowgraph_wikival.keys():
        treat_knowgraph_wikival[code] = []
    
print('len sosy val', len(sosy_knowgraph_wikival))
print('len treat val', len(treat_knowgraph_wikival))
print('len codes', len(ICD9CODES))
assert sosy_knowgraph_wikival.keys() == ICD9CODES.keys()
assert treat_knowgraph_wikival.keys() == ICD9CODES.keys()
'''
--------> SOSY - TP: 2437, FP: 422, Precision: 0.8523959426372858
--------> TREATMENT - TP: 2976, FP: 1005, Precision: 0.747550866616428
--------> OVERALL - TP: 5413, FP: 1427, Precision: 0.791374269005848
'''


with open('GPT4_sosy_knowgraph_wikival.json', 'w') as f:
    json.dump(sosy_knowgraph_wikival, f)

with open('GPT4_treat_knowgraph_wikival.json', 'w') as f:
    json.dump(treat_knowgraph_wikival, f)