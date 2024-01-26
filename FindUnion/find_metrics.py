import json



# find number of nodes and edges for sosy

# find number of nodes and edges for treat


# find number of nodes agree, wikionly, mayo only
with open('final_sosy_knowgraph_metrics.json', 'r') as f:
    sosy_metrics = json.load(f)

with open('final_treat_knowgraph_metrics.json', 'r') as f:
    treat_metrics = json.load(f)
tot_agree1 = 0
tot_wikionly1 = 0
tot_mayoonly1 = 0
for icd, metrics in sosy_metrics.items():
    tot_agree1 += metrics[0]
    tot_wikionly1 += metrics[1]
    tot_mayoonly1 += metrics[2]
tot_agree2 = 0
tot_wikionly2 = 0
tot_mayoonly2 = 0
for icd, metrics in treat_metrics.items():
    tot_agree2 += metrics[0]
    tot_wikionly2 += metrics[1]
    tot_mayoonly2 += metrics[2]
print(f'SOSY: # nodes agree: {tot_agree1}, # nodes wikionly: {tot_wikionly1}, # nodes mayoonly: {tot_mayoonly1}')
print(f'TREAT: # nodes agree: {tot_agree2}, # nodes wikionly: {tot_wikionly2}, # nodes mayoonly: {tot_mayoonly2}')
print(f'TOTAL: # nodes agree: {tot_agree1+tot_agree2}, # nodes wikionly: {tot_wikionly1+tot_wikionly2}, # nodes mayoonly: {tot_mayoonly1+tot_mayoonly2}')