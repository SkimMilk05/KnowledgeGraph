from openai import OpenAI
import pickle
import json
OPENAI_API_KEY='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'

client = OpenAI(api_key=OPENAI_API_KEY)

with open('gpt4resp_p1.pkl', 'rb') as f:
    treat_resp_p1, sosy_resp_p1 = pickle.load(f)

with open('finalwikidict.pkl', 'rb') as f:
    pages = pickle.load(f)

treat_resp_p2 = dict()
sosy_resp_p2  = dict()
failed = set()

for key, page in pages.items():
    icd = key[:key.index(':')]
    disease = key[key.rindex(':') + 1 :]
    icdd = f'{icd}: {disease}'

    try:
        # treatments
        if icdd not in treat_resp_p1:
            print(f'Querying treatment - {icdd}')
            completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are a professional clinician, skilled in clinical concepts and medical knowledge"},
                {"role": "user", "content": f"Create a bulleted list of treatments for {disease} that are mentioned in the following text: {page}."},
            ]
            )
            resp = str(completion.choices[0].message)
            treat_resp_p2[icdd] = resp

        # signs and symptoms
        if icdd not in sosy_resp_p1:
            print(f'Querying sosy - {icdd}')
            completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are a professional clinician, skilled in clinical concepts and medical knowledge"},
                {"role": "user", "content": f"Create a bulleted list of signs and symptoms for {disease} that are mentioned in the following text: {page}."},
            ]
            )
            resp = str(completion.choices[0].message)
            sosy_resp_p2[icdd] = resp

    except Exception as e:
        print('=========EXCEPTION!================')
        print(f'Cause of exception - {icdd}')
        print(e)
        failed.add(icdd)
        print('===============================')



with open('gpt4resp_p2.pkl', 'wb') as f:
    pickle.dump((treat_resp_p2, sosy_resp_p2), f)

with open('gpt4resp_treat_p2.json', 'w') as f:
    json.dump(treat_resp_p2, f)

with open('gpt4resp_sosy_p2.json', 'w') as f:
    json.dump(sosy_resp_p2, f)