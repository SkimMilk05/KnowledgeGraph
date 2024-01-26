'''
Extract MM objects directly from wikipedia pages
'''

import pickle 
from pymetamap import MetaMap
# from metamap_configs import metamap_base_dir, metamap_bin_dir
import json

from itertools import islice

metamap_base_dir = '/home/cogems_nist/Desktop/NewModel/public_mm/'
metamap_bin_dir = '/bin/metamap20'
metamap_pos_server_dir = 'bin/skrmedpostctl'
metamap_wsd_server_dir = 'bin/wsdserverctl'

dir = metamap_base_dir + metamap_bin_dir
metam = MetaMap.get_instance(dir)

with open('finalwikidict.pkl', 'rb') as f:
    finalwikidict = pickle.load(f)

sosy_mmresp = dict()
treat_mmresp = dict()

for k, content in finalwikidict.items():
    # get icd9 code
    # icd9 = k[:k.index(':')]
    icdd = k[:k.index(':')] +  k[k.rindex(':'):]
    print(f"==========Processing {icdd}=============")

    try:
        # extract sosy
        sign_concepts, errs = metam.extract_concepts([content],
                                word_sense_disambiguation = True,
                                # Sign or Symptom, Disease or Syndrome, Mental or Behavioral Dysfunction
                                restrict_to_sts = ['sosy', 'dsyn', 'mobd'],
                                composite_phrase = 1, # for memory issues
                                prune = 30,
                                )
        sosy_mmresp[icdd] = sign_concepts
    except Exception as e:
        print('=========ERROR================')
        print(e)

    try:
        # extract reatment
        treat_concepts, errs = metam.extract_concepts([content],
                                    word_sense_disambiguation = True,
                                    # Therapeutic or Preventive Procedure
                                    # Antibotic, Clinical Drug, Vitamin, Organic Chemical, Inorganic Chemical
                                    restrict_to_sts = ['topp',
                                                    'antb', 'clnd', 'vita', 'orch', 'inch', 'aapp'
                                    ],
                                    composite_phrase = 1, # for memory issues
                                    prune = 30)
        treat_mmresp[icdd] = treat_concepts
    except Exception as e:
        print('=========ERROR================')
        print(e)

# save dicts to json
with open("wiki_sosy_mm_objects.json", "w") as f:
    json.dump(sosy_mmresp, f)
# save dicts to json
with open("wiki_treat_mm_objects.json", "w") as f:
    json.dump(treat_mmresp, f)