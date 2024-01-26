import json
import sys
sys.path.append('../')
from utils import GENERAL_TERMS

# ====== sosy ==========================================
with open('GPT4_sosy_mm_objects.json', 'r') as f:
    sosy_mm_objects = json.load(f)

print("len keys sosy mm", len(sosy_mm_objects.keys()))
sosy_knowgraph = dict()
for icdd, list_concepts in sosy_mm_objects.items():
    set_concepts = set()
    [set_concepts.add(concept[3].lower()) for concept in list_concepts if concept[1] == 'MMI' and concept[3].lower() not in GENERAL_TERMS]
    sosy_knowgraph[icdd[:icdd.index(':')]] = list(set_concepts)

print("len keys sosy knowgraph", len(sosy_knowgraph.keys()))
with open('GPT4_sosy_knowgraph.json', 'w') as f:
    json.dump(sosy_knowgraph, f)

# ====== treatment ==========================================
with open('GPT4_treat_mm_objects.json', 'r') as f:
    treat_mm_objects = json.load(f)

print("len keys treat mm", len(treat_mm_objects.keys()))
treat_knowgraph = dict()
for icdd, list_concepts in treat_mm_objects.items():
    set_concepts = set()
    [set_concepts.add(concept[3].lower()) for concept in list_concepts if concept[1] == 'MMI' and concept[3].lower() not in GENERAL_TERMS]
    treat_knowgraph[icdd[:icdd.index(':')]] = list(set_concepts)
print("len keys treat knowgraph", len(treat_knowgraph.keys()))

with open('GPT4_treat_knowgraph.json', 'w') as f:
    json.dump(treat_knowgraph, f)