import json
import sys
sys.path.append('../')
from utils import ICD9CODES, GENERAL_TERMS

with open('mayo_sosy_knowgraph.json', 'r') as f:
    mayo_sosy_knowgraph = json.load(f)

with open('mayo_treat_knowgraph.json', 'r') as f:
    mayo_treat_knowgraph = json.load(f)

with open('GPT4_sosy_knowgraph_wikival.json', 'r') as f:
    GPT4_sosy_knowgraph_wikival = json.load(f)

with open('GPT4_treat_knowgraph_wikival.json', 'r') as f:
    GPT4_treat_knowgraph_wikival = json.load(f)

# ==== sosy ======================================
final_sosy_knowgraph = dict()
final_sosy_knowgraph_metrics = dict() #agree, wikionly, mayoonly
for icd, wikilist in GPT4_sosy_knowgraph_wikival.items():
    print(f'=========SOSY: {icd}===============')
    try:
        wiki_set = set(wikilist)
        mayo_set = set(mayo_sosy_knowgraph[icd])
        union_set = wiki_set.union(mayo_set)
        wikionly = len(union_set) - len(mayo_set)
        mayoonly = len(union_set) - len(wiki_set)
        agree = len(union_set) - wikionly - mayoonly
        final_sosy_knowgraph[icd] = list(union_set)
        final_sosy_knowgraph_metrics[icd] = (agree, wikionly, mayoonly)
        print(f'wikiset: {wiki_set}')
        print(f'mayoset: {mayo_set}')
        print(f'unionset:{union_set}')
        print(f'agree: {agree}, wikionly: {wikionly}, mayoonly: {mayoonly}')
    except KeyError:
        final_sosy_knowgraph[icd] = list(wiki_set)
        final_sosy_knowgraph_metrics[icd] = (0, len(wiki_set), 0)
        continue

with open('final_sosy_knowgraph.json', 'w') as f:
    json.dump(final_sosy_knowgraph, f)

with open('final_sosy_knowgraph_metrics.json', 'w') as f:
    json.dump(final_sosy_knowgraph_metrics, f)


# ==== treat ======================================
final_treat_knowgraph = dict()
final_treat_knowgraph_metrics = dict() #agree, wikionly, mayoonly
for icd, wikilist in GPT4_treat_knowgraph_wikival.items():
    print(f'=========TREATMENT: {icd}===============')
    try:
        wiki_set = set(wikilist)
        mayo_set = set(mayo_treat_knowgraph[icd])
        union_set = wiki_set.union(mayo_set)
        wikionly = len(union_set) - len(mayo_set)
        mayoonly = len(union_set) - len(wiki_set)
        agree = len(union_set) - wikionly - mayoonly
        final_treat_knowgraph[icd] = list(union_set)
        final_treat_knowgraph_metrics[icd] = (agree, wikionly, mayoonly)
        print(f'wikiset: {wiki_set}')
        print(f'mayoset: {mayo_set}')
        print(f'agree: {agree}, wikionly: {wikionly}, mayoonly: {mayoonly}')
    except KeyError:
        final_treat_knowgraph[icd] = list(wiki_set)
        final_treat_knowgraph_metrics[icd] = (0, len(wiki_set), 0)
        continue

# === sanity check
print(len(final_sosy_knowgraph.keys()))
print(len(ICD9CODES.keys()))
assert final_sosy_knowgraph.keys() == ICD9CODES.keys()

print(len(final_treat_knowgraph.keys()))
print(len(ICD9CODES.keys()))
assert final_treat_knowgraph.keys() == ICD9CODES.keys()

for list in final_sosy_knowgraph.values():
    for item in list:
        assert item not in GENERAL_TERMS

for list in final_treat_knowgraph.values():
    for item in list:
        assert item not in GENERAL_TERMS

count = 0
for icd in mayo_sosy_knowgraph.keys():
    if icd not in GPT4_sosy_knowgraph_wikival.keys(): count += 1
print('Number of pages in mayo clinic not found in wiki', count)

print(f'Number of pages in mayo clinic: {len(mayo_sosy_knowgraph)} out of {len(ICD9CODES)}, {len(mayo_sosy_knowgraph)/len(ICD9CODES)}')

# ===== end check ============

with open('final_treat_knowgraph.json', 'w') as f:
    json.dump(final_treat_knowgraph, f)

with open('final_treat_knowgraph_metrics.json', 'w') as f:
    json.dump(final_treat_knowgraph_metrics, f)
