import os
from time import sleep
from metamap_configs import metamap_base_dir, metamap_pos_server_dir, metamap_wsd_server_dir

# Start servers
os.system(metamap_base_dir + metamap_pos_server_dir + ' start') # Part of speech tagger
os.system(metamap_base_dir + metamap_wsd_server_dir + ' start') # Word sense disambiguation 

# Sleep a bit to give time for these servers to start up
sleep(20)

print("Metamap servers are up!")