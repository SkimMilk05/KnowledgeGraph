from openai import OpenAI
import pickle
import json
OPENAI_API_KEY='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'

client = OpenAI(api_key=OPENAI_API_KEY)


with open('finalwikidict.pkl', 'rb') as f:
    pages = pickle.load(f)

treat_resp_p3 = dict()
sosy_resp_p3  = dict()
failed = set()

missing_icdds =  ["427.5: Cardiac Arrest: Cardiac arrest", "285.9: Anemia: Anemia"]

for key in missing_icdds:
    page = pages[key]
    icd = key[:key.index(':')]
    disease = key[key.rindex(':') + 1 :]
    icdd = f'{icd}: {disease}'

    try:
        # treatments
        print(f'Querying treatment - {icdd}')
        completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a professional clinician, skilled in clinical concepts and medical knowledge"},
            {"role": "user", "content": f"Create a bulleted list of treatments for {disease} that are mentioned in the following text: {page}."},
        ]
        )
        resp = str(completion.choices[0].message)
        treat_resp_p3[icdd] = resp

        # signs and symptoms
        print(f'Querying sosy - {icdd}')
        completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a professional clinician, skilled in clinical concepts and medical knowledge"},
            {"role": "user", "content": f"Create a bulleted list of signs and symptoms for {disease} that are mentioned in the following text: {page}."},
        ]
        )
        resp = str(completion.choices[0].message)
        sosy_resp_p3[icdd] = resp

    except Exception as e:
        print('=========EXCEPTION!================')
        print(f'Cause of exception - {icdd}')
        print(e)
        failed.add(icdd)
        print('===============================')



with open('gpt4resp_p3.pkl', 'wb') as f:
    pickle.dump((treat_resp_p3, sosy_resp_p3), f)

with open('gpt4resp_treat_p3.json', 'w') as f:
    json.dump(treat_resp_p3, f)

with open('gpt4resp_sosy_p3.json', 'w') as f:
    json.dump(sosy_resp_p3, f)