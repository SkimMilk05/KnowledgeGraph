import json
from utils import GENERAL_TERMS

with open('GPT4_treat_knowgraph.json', 'r') as f:
    d = json.load(f)

new_d = dict()
for k, v_list in d.items():
    new_d[k] = [v for v in v_list if v not in GENERAL_TERMS]

with open('GPT4_treat_knowgraph_filtered.json', 'w') as f:
    json.dump(new_d, f)