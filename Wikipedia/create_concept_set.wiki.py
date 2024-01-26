'''
    This script creates a set of metamap concepts mentioned on each wikipedia page
    from metamap response objects
'''

import json

with open('wiki_sosy_mm_objects.json', 'r') as f:
    sosy_MM_resp = json.load(f)

with open('wiki_treat_mm_objects.json', 'r') as f:
    treat_MM_resp = json.load(f)

sosy_setSs = dict()
for icdd, list_concepts in sosy_MM_resp.items():
    icd = icdd[:icdd.index(':')]
    setS = []
    for concept in list_concepts:
        setS.append(concept[3].lower()) #index 3 is the string of the concept
    sosy_setSs[icd] = setS

treat_setSs = dict()
for icdd, list_concepts in treat_MM_resp.items():
    icd = icdd[:icdd.index(':')]
    setS = []
    for concept in list_concepts:
        setS.append(concept[3].lower()) #index 3 is the string of the concept
    treat_setSs[icd] = setS

with open('wiki_sosy_sets.json', 'w') as f:
    json.dump(sosy_setSs, f)

with open('wiki_treat_sets.json', 'w') as f:
    json.dump(treat_setSs, f)
