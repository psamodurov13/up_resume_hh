from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests as rq
import random as rd
import auth_data as ad

# Connect webdriver Chrome
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36')


# Get cookies
def get_cookies():
    cookies = {}
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']
    return cookies


def main():
    driver.get('https://hh.ru/')
    time.sleep(3)
    cookies = driver.get_cookies()[1]
    s = rq.Session()
    s.cookies.set(domain=cookies['domain'], name=cookies['name'], path=cookies['path'], value=cookies['value'])
    # Open auth page
    driver.get('https://hh.ru/account/login?backurl=%2F%3FhhtmFrom%3Daccount_login&hhtmFrom=main')
    # Select login by e-mail and password
    to_email = driver.find_element(By.CSS_SELECTOR, '.account-login-actions .bloko-link_pseudo')
    to_email.click()
    time.sleep(3)
    # Fill email
    username_input = driver.find_element(By.CSS_SELECTOR, '.bloko-input-text-wrapper input[name="username"]')
    username_input.send_keys(ad.login)
    time.sleep(2)
    # Fill password
    password_input = driver.find_element(By.CSS_SELECTOR, '.bloko-input-text-wrapper input[type="password"]')
    password_input.send_keys(ad.password)
    time.sleep(5)
    # Press on button "Войти"
    go = driver.find_element(By.CSS_SELECTOR, 'button[data-qa="account-login-submit"]')
    go.click()
    # Timeout for possible capcha
    time.sleep(35)

    while True:
        # Open resume page and press on button "поднять" (update)
        resumes = [
            'https://hh.ru/resume/f2044f8fff0b4653c60039ed1f4a5256587634',
            'https://hh.ru/resume/9659655cff0b5162360039ed1f4a4d65457730'
        ]
        for i in resumes:
            driver.get(i)
            up_resume = driver.find_element(By.CSS_SELECTOR,
                                            '.resume-applicant > .resume-wrapper button[data-qa="resume-update-button"]')
            up_resume.click()
            time.sleep(10)
        # For next 4 hours start cycle open pages with random timeout. Than update resume again
        urls = [
            'https://hh.ru/articles/market-news/hr-news?from=footer_new&hhtmFromLabel=footer_new&hhtmFrom=main',
            'https://hh.ru/?hhtmFromLabel=header&hhtmFrom=resume_list',
            'https://hh.ru/',
            'https://hh.ru/metro?from=footer_new&hhtmFromLabel=footer_new&hhtmFrom=articles',
            'https://hh.ru/applicant/negotiations?hhtmFromLabel=header&hhtmFrom=main',
            'https://hh.ru/employers_company?from=footer_new&hhtmFromLabel=footer_new&hhtmFrom=negotiation_list',
            'https://hh.ru/expert_resume?hhtmFromLabel=header&hhtmFrom=employer_search_catalog'
        ]
        all_timeout = 0
        goal = 14400
        while True:
            if goal - all_timeout > 900:
                timeout = rd.randint(400, 900)
                print('no_last')
            else:
                timeout = goal - all_timeout + 20
                print('last')
            driver.get(rd.choice(urls))
            time.sleep(timeout)
            print('timeout', timeout)
            all_timeout += timeout
            print('all_timeout', all_timeout)
            if all_timeout > goal:
                break


if __name__ == '__main__':
    main()
