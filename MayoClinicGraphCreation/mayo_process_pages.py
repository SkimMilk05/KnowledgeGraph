from bs4 import BeautifulSoup
import json

with open('responses.json', 'r') as f:
    resp_dict = json.load(f)

mayo_sosy_lists = dict()
mayo_treat_lists = dict()
fails = []

for icdd, urls in resp_dict.items():
    print(f'============{icdd}==============')
    term = icdd[icdd.index(':')+2:].replace(' ', '%20')
    try:
        # ======= sosy ===========================
        with open(f'htmlpages/{term}_sosy.html', 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        sosy_list = soup.find('h2',string='Symptoms').find_next('ul')
        mayo_sosy_lists[icdd] = [li.text for li in sosy_list if li.text != '\n']
        print('extracted sosy list from html')
        # ======= treatment ========================
        if urls[1] == 'None': continue # check if there is treatment page
        with open(f'htmlpages/{term}_treat.html', 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        result = soup.find('h2',string='Treatment').find_all_next()
        treat_section = ''
        for tag in result:
            if tag.name == 'h2': break
            treat_section += tag.get_text(strip=True)
        mayo_treat_lists[icdd] = treat_section
        print('extracted treament section from html')
    except AttributeError:
        print("FAIL")
        fails.append(icdd)

with open("mayo_sosy_lists.json", "w") as f:
    json.dump(mayo_sosy_lists, f)

with open("mayo_treat_lists.json", "w") as f:
    json.dump(mayo_treat_lists, f)

print('FAILED ICD9 CODES:')
print(fails)

'''
Fails:
['430: Subarachnoid hemorrhage', '431: Intracerebral hemorrhage', '772.10: Intraventricular hemorrhage', 'E878.8: Surgery', 'E879.8: Surgery']
'''