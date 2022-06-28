import pickle
import random
import time

from django.utils.encoding import smart_str
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
chrome_options = Options()
chrome_options.add_argument("--headless")

# driver = webdriver.Chrome('/home/webtunixhaz/Videos/linkdin_automation/chromedriver',options=chrome_options)
driver = webdriver.Chrome('./chromedriver')
action = ActionChains(driver)

def login(USERNAME,PASSWORD):

    driver.get('https://www.linkedin.com/')
    xx = os.path.exists('./linkdin_automation/'+str(USERNAME)+'.pkl')
    if xx:
        cookies = pickle.load(open("./linkdin_automation/"+str(USERNAME)+".pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    else:
        # driver.get('https://www.linkedin.com/')
        time.sleep(5)
        username = driver.find_element_by_name('session_key')
        username.clear()
        username.send_keys(USERNAME)
        password = driver.find_element_by_name("session_password")
        password.clear()
        password.send_keys(PASSWORD)
        driver.find_element_by_class_name("sign-in-form__submit-button").click()
        pickle.dump(driver.get_cookies(), open("/home/webtunix/Desktop/linkdin_automation/"+str(USERNAME)+".pkl", "wb"))



def sales(USERNAME,PASSWORD,GLOBAL_SEARCH,LOCATIONS, INDUSTRIES,TITLE):
    login(USERNAME,PASSWORD)
    driver.get('https://www.linkedin.com/sales/home')
    time.sleep(7)
    global_search_input = driver.find_element_by_id('global-typeahead-search-input')
    global_search_input.clear()
    global_search_input.send_keys(GLOBAL_SEARCH)
    driver.get('https://www.linkedin.com/sales/search/people?viewAllFilters=true')
    time.sleep(10)

    actions = ActionChains(driver)

    keywords_=driver.find_element_by_xpath("//fieldset[@data-test-search-filter='POSTED_CONTENT_KEYWORDS']").click()
    keywords = driver.find_element_by_xpath("//*[@placeholder='Add keywords']")
    keywords.send_keys(GLOBAL_SEARCH)
    keywords.send_keys(Keys.TAB)
    time.sleep(2)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    time.sleep(3)



    locationn = driver.find_element_by_xpath("//fieldset[@data-test-search-filter='GEOGRAPHY']").click()
    time.sleep(2)

    add_location = driver.find_element_by_xpath("//*[@placeholder='Add locations']")
    add_location.send_keys(LOCATIONS)
    time.sleep(3)
    add_location.send_keys(Keys.TAB)
    time.sleep(2)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    time.sleep(3)

    industry = driver.find_element_by_xpath("//fieldset[@data-test-search-filter='INDUSTRY']").click()
    time.sleep(2)
    add_industry = driver.find_element_by_xpath("//*[@placeholder='Add industries']")
    add_industry.send_keys(INDUSTRIES)
    time.sleep(3)

    add_industry.send_keys(Keys.TAB)
    time.sleep(2)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    time.sleep(2)

    title=driver.find_element_by_xpath("//fieldset[@data-test-search-filter='TITLE']").click()
    time.sleep(2)
    add_title = driver.find_element_by_xpath("//*[@placeholder='Add titles']")
    add_title.send_keys(TITLE)
    time.sleep(3)
    actions.send_keys(Keys.TAB)
    time.sleep(2)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    time.sleep(2)
    # search = driver.find_element_by_xpath("//*[@data-control-name='advanced_search_profile']").click()
    time.sleep(3)
    url =smart_str(driver.current_url)
    print(url)
    return url





def extraction(USERNAME,PASSWORD,GLOBAL_SEARCH,LOCATIONS,INDUSTRIES,TITLE):
    url =sales(USERNAME, PASSWORD, GLOBAL_SEARCH, LOCATIONS, INDUSTRIES, TITLE)
    time.sleep(6)
    linkss = []
    print(url)
    print('ppppppppppppppppppppppppppppppppppppppppppppppp')
    profile_links = []
    for i in range(1, 2):
        print(i)
        # aa_1 = url.split('page=')
        # aa = aa_1[0] + str('page=') + str(i) + aa_1[1]
        # driver.get(aa)
        driver.get(url)
        time.sleep(random.randint(9, 20))
        SCROLL_PAUSE_TIME = random.randint(2, 6)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            vv = driver.find_elements_by_xpath("//a[@data-control-name='view_profile_via_result_name']")
            profile_links.extend(vv)
            driver.execute_script("window.scrollTo(0, window.scrollY + 500);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        vv = list(set(profile_links))
        print(vv)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
        for m in vv:
            links = m.get_attribute('href')
            linkss.append(links)
    linkss = set(linkss)
    return linkss

#
def send_requests(USERNAME,PASSWORD,GLOBAL_SEARCH,LOCATIONS,INDUSTRIES,TITLE,MESSAGE):
    urls = extraction(USERNAME,PASSWORD,GLOBAL_SEARCH,LOCATIONS,INDUSTRIES,TITLE)
    for i in urls:
        try:
            time.sleep(6)
            driver.get(str(i))
            time.sleep(15)
            search = driver.find_element_by_xpath("//div[@class='artdeco-dropdown artdeco-dropdown--placement-bottom artdeco-dropdown--justification-right ember-view']").click()
            time.sleep(4)
            connect = driver.find_element_by_xpath("//div[@data-control-name='connect']").click()
            time.sleep(4)
            message = driver.find_element_by_xpath("//*[@data-test-connect-cta='textarea']")
            message.send_keys(MESSAGE)
            time.sleep(3)
            send = driver.find_element_by_xpath("//button[@data-test-connect-cta='send']").click()
        except:
            print(i)





USERNAME ='electronomius@gmail.com'
PASSWORD = ''
GLOBAL_SEARCH = "CTO"
LOCATIONS='CANADA'
INDUSTRIES='ELECTRIC'
TITLE ='CTO'
MESSAGE ='HELLO'

#
# login(USERNAME,PASSWORD)
# driver.get(str('https://www.linkedin.com/sales/people/ACwAAAZ57c8Bvya8Y0KLtxvaFOMzgbyFhvFQ5JM,NAME_SEARCH,z59O?_ntb=SJUZtAg7SlqvGrDzqWZzuw%3D%3D'))
# time.sleep(15)
# search = driver.find_element_by_xpath("//button[@id='ember79']").click()
# time.sleep(4)
# connect = driver.find_element_by_xpath("//div[@data-control-name='connect']").click()
# time.sleep(4)
# message = driver.find_element_by_xpath("//*[@data-test-connect-cta='textarea']")
# message.send_keys(MESSAGE)
# time.sleep(3)
# send = driver.find_element_by_xpath("//button[@data-test-connect-cta='send']").click()



send_requests(USERNAME,PASSWORD,GLOBAL_SEARCH,LOCATIONS,INDUSTRIES,TITLE,MESSAGE)

