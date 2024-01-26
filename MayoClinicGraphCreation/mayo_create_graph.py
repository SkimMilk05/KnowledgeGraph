import json
import sys
sys.path.append('../')
from utils import GENERAL_TERMS

# ====== sosy ==========================================
with open('mayo_sosy_mm_objects.json', 'r') as f:
    mayo_sosy_mm_objects = json.load(f)

mayo_sosy_knowgraph = dict()
for icdd, list_concepts in mayo_sosy_mm_objects.items():
    set_concepts = set()
    [set_concepts.add(concept[3].lower()) for concept in list_concepts if concept[1] == 'MMI' and concept[3].lower() not in GENERAL_TERMS]
    mayo_sosy_knowgraph[icdd[:icdd.index(':')]] = list(set_concepts)

with open('mayo_sosy_knowgraph.json', 'w') as f:
    json.dump(mayo_sosy_knowgraph, f)

# ====== treatment ==========================================
with open('mayo_treat_mm_objects.json', 'r') as f:
    mayo_treat_mm_objects = json.load(f)

mayo_treat_knowgraph = dict()
for icdd, list_concepts in mayo_treat_mm_objects.items():
    set_concepts = set()
    [set_concepts.add(concept[3].lower()) for concept in list_concepts if concept[1] == 'MMI' and concept[3].lower() not in GENERAL_TERMS]
    mayo_treat_knowgraph[icdd[:icdd.index(':')]] = list(set_concepts)

with open('mayo_treat_knowgraph.json', 'w') as f:
    json.dump(mayo_treat_knowgraph, f)