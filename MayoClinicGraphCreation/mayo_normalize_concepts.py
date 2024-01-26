import sys
sys.path.append('../')
from pymetamap import MetaMap
from Metamap.metamap_configs import dir

import json

metam = MetaMap.get_instance(dir)

# ======= SOSY ========================
mayo_sosy_mm_objects = dict()
with open('mayo_sosy_lists.json', 'r') as f:
    mayo_sosy_lists = json.load(f)
for icdd, list_str in mayo_sosy_lists.items():
    try:
        print(f"Normalizing SOSY for {icdd}")
        mayo_sosy_mm_objects[icdd] = []
        for str in list_str:
            # find UMLS sosy concepts and add them to set
            concepts, errs = metam.extract_concepts([str],
                                    word_sense_disambiguation = True,
                                    # Sign or Symptom, Disease or Syndrome, Mental or Behavioral Dysfunction
                                    restrict_to_sts = ['sosy', 'dsyn', 'mobd'],
                                    composite_phrase = 1, # for memory issues
                                    prune = 30,
                                    )
            [mayo_sosy_mm_objects[icdd].append(concept) for concept in concepts]
    except Exception as e:
        print('=========ERROR================')
        print(e)

with open('mayo_sosy_mm_objects.json', 'w') as f:
    json.dump(mayo_sosy_mm_objects, f)

# ========= TREATMENT =============
mayo_treat_mm_objects = dict()
with open('mayo_treat_lists.json', 'r') as f:
    mayo_treat_lists = json.load(f)

for icdd, str in mayo_treat_lists.items():
    try:
        print(f"Normalizing TREATMENTS for {icdd}")
        # find UMLS treatment concepts and add them to set
        concepts, errs = metam.extract_concepts([str],
                                word_sense_disambiguation = True,
                                # Therapeutic or Preventive Procedure
                                # Antibotic, Clinical Drug, Vitamin, Organic Chemical, Inorganic Chemical
                                restrict_to_sts = ['topp',
                                                'antb', 'clnd', 'vita', 'orch', 'inch', 'aapp'
                                ],
                                composite_phrase = 1, # for memory issues
                                prune = 30,
                                )
        mayo_treat_mm_objects[icdd] = [concept for concept in concepts]
    except Exception as e:
        print('=========ERROR================')
        print(e)

with open('mayo_treat_mm_objects.json', 'w') as f:
    json.dump(mayo_treat_mm_objects, f)

