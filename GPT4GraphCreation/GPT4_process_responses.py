import pickle
import re
import json

with open('gpt4resp_p1.pkl', 'rb') as f:
    treat_resp_p1, sosy_resp_p1 = pickle.load(f)

with open('gpt4resp_p2.pkl', 'rb') as f:
    treat_resp_p2, sosy_resp_p2 = pickle.load(f)

with open('gpt4resp_p3.pkl', 'rb') as f:
    treat_resp_p3, sosy_resp_p3 = pickle.load(f)

treat_resp = treat_resp_p1 | treat_resp_p2 | treat_resp_p3
sosy_resp = sosy_resp_p1 | sosy_resp_p2 | sosy_resp_p3

treat_lists = dict()
sosy_lists = dict()

new_treat_resp = dict()
new_sosy_resp = dict()

unique_treat = dict()
unique_sosy = dict()

for k, resp in treat_resp.items():
    key = k.replace(':  ', ': ')
    _, content = re.split('content=["\']', resp)
    content, _ = re.split('["\'], role=', content)
    # make filtered list
    concepts = []
    for item in content.split('\\n'):
        # if list item (and not description/header, add to concepts)
        if ('- ' in item ) or ('* ' in item):
            concept = item.replace('**', '').strip()[2:]
            concepts.append(concept) 
            if concept not in unique_treat: unique_treat[concept] = []
            unique_treat[concept].append(key)
    # add to knowledge map
    treat_lists[key] = concepts
    new_treat_resp[key] = resp

for k, resp in sosy_resp.items():
    key = k.replace(':  ', ': ')
    _, content = re.split('content=["\']', resp)
    content, _ = re.split('["\'], role=', content)
    # make filtered list
    concepts = []
    for item in content.split('\\n'):
        if ('- ' in item ) or ('* ' in item):
            concept = item.replace('**', '').strip()[2:]
            concepts.append(concept) 
            if concept not in unique_sosy: unique_sosy[concept] = []
            unique_sosy[concept].append(key)
    # add to knowledge map
    sosy_lists[key] = concepts
    new_sosy_resp[key] = resp


with open('gpt4_resp_treat.json', 'w') as f:
    json.dump(new_treat_resp, f)

with open('gpt4_resp_sosy.json', 'w') as f:
    json.dump(new_sosy_resp, f)

with open('GPT4_treat_lists.json', 'w') as f:
    json.dump(treat_lists, f)

with open('GPT4_sosy_lists.json', 'w') as f:
    json.dump(sosy_lists, f)