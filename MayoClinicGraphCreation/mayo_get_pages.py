from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import json
import sys

with open('sosy_know_map.json', 'r') as f:
    sosy_know_map= json.load(f)
    icdds = list(sosy_know_map.keys())

xpath_sosy_link = '//*[@id="cmp-skip-to-main__content"]/ul/li/h3/div/a'
xpath_search_instead = '//*[@id="cmp-skip-to-main__content"]/div/ul[1]/li[2]/div/a'

chrome_options = Options()
chrome_options.add_argument("--headless=new") # for Chrome >= 109
chrome_options.add_argument("--enable-chrome-browser-cloud-management")
responses = dict()
no_responses = dict()

try:
    count = 0
    for icdd in icdds:
        count += 1
        try:
            driver = webdriver.Chrome(options=chrome_options)
            term = icdd[icdd.index(':')+2:].replace(' ', '%20')
            print(f'----------({count}/{len(icdds)}) {icdd}--------------')
        # SEARCH FOR LINK TO PAGE
            # search the term, try getting first result
            try:
                searchURL = f'https://www.mayoclinic.org/diseases-conditions/search-responses?q={term}'
                driver.get(searchURL)
                sosypageURL = driver.find_element("xpath", xpath_sosy_link).get_attribute("href")

            # if there is no first result, take the "Did you mean to search for..?" link
            except NoSuchElementException:
                try:
                    print(f'Taking the "Did you mean..?" link for {term}')
                    searchURL = driver.find_element("xpath", xpath_search_instead).get_attribute("href")
                    print(f'Redirecting to {searchURL}')
                    driver.get(searchURL)
                    sosypageURL = driver.find_element("xpath", xpath_sosy_link).get_attribute("href")
                # there is no result in Dieases & Conditions. Do this one manually later
                except NoSuchElementException:
                    print(f'No responses for {term}')
                    no_responses[icdd] = ('No responses', '')
                    continue
        except Exception as e:
            print("UNHANDLED ERROR!!")
            _, _, exc_tb = sys.exc_info()
            no_responses[icdd] = (e,  exc_tb.tb_lineno)

    # GET PAGE
        print(f'Found responses for {term}')
        xpath_treat_link = "/html/body//a[contains(@href,'diagnosis-treatment')]"
        
        # get signs and symptoms page
        driver.get(sosypageURL)
        # save html search responses page
        with open(f'htmlpages/{term}_sosy.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print('sosy page saved')

        # get the treatment page
        try:
            treatpageURL = driver.find_element("xpath", xpath_treat_link).get_attribute("href")
            driver.get(treatpageURL)
            # save html search responses page
            with open(f'htmlpages/{term}_treat.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print('treat page saved')
        except NoSuchElementException:
            print(f'Treatment link error for {term}')
            treatpageURL = 'None'

        # save links
        responses[icdd] = (sosypageURL, treatpageURL)
        
        # close driver
        driver.close()

finally:
    # write responses
    with open("responses.json", "w") as f:
        json.dump(responses, f)

    with open("no_responses.json", "w") as f:
        json.dump(no_responses, f)

    print(f'Number icd codes: {len(icdds)}, responses for: {len(responses)}, No responses for: {len(no_responses)}')
    # Number icd codes: 220, responses for: 135, No responses for: 85