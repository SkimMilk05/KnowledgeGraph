from openai import OpenAI
import pickle
import json
OPENAI_API_KEY='<put your api key here>'

client = OpenAI(api_key=OPENAI_API_KEY)

with open('finalwikidict.pkl', 'rb') as f:
    pages = pickle.load(f)

treat_resp = dict()
sosy_resp = dict()
for key, page in pages.items():
    try:
        icd = key[:key.index(':')]
        disease = key[key.rindex(':') + 1 :]
        print(f'Processing {icd}: {disease}')

        # treatments
        completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a professional clinician, skilled in clinical concepts and medical knowledge"},
            {"role": "user", "content": f"Create a bulleted list of treatments for {disease} that are mentioned in the following text: {page}."},
        ]
        )
        resp = str(completion.choices[0].message)
        treat_resp[f'{icd}: {disease}'] = resp

        # signs and symptoms
        completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a professional clinician, skilled in clinical concepts and medical knowledge"},
            {"role": "user", "content": f"Create a bulleted list of signs and symptoms for {disease} that are mentioned in the following text: {page}."},
        ]
        )
        resp = str(completion.choices[0].message)
        sosy_resp[f'{icd}: {disease}'] = resp
    except Exception as e:
        print('=========EXCEPTION!================')
        print(f'Cause of exception - {icd}: {disease}')
        print(e)
        print('===============================')



with open('gpt4resp.pkl', 'wb') as f:
    pickle.dump((treat_resp, sosy_resp),f)

with open('gpt4resp_treat_p1.json', 'w') as f:
    json.dump(treat_resp, f)

with open('gpt4resp_sosy_p1.json', 'w') as f:
    json.dump(sosy_resp, f)
