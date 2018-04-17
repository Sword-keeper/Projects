from Spiders.tools import generate_url, get_page, WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import selenium.webdriver.support.ui as ui
import json

# https://www.kickstarter.com/discover/advanced?staff_picks=1&sort=popularity&seed=2537785&page=1
base = 'https://www.kickstarter.com/discover/advanced'

collected_hrefs = [
    'https://www.kickstarter.com/projects/1227872561/unbroken-a-solo-game-of-survival-and-revenge?ref=discovery',
    'https://www.kickstarter.com/projects/moment/the-future-of-mobile-filmmaking-anamorphic-battery?ref=discovery',
    'https://www.kickstarter.com/projects/kingartgames/iron-harvest?ref=discovery',
    'https://www.kickstarter.com/projects/pandasaurus/dinosaur-island-back-from-extinction?ref=discovery',
    'https://www.kickstarter.com/projects/625059603/the-micro-wallet-doing-more-with-less?ref=discovery',
    'https://www.kickstarter.com/projects/naran/microbot-sense-smart-sensor-for-smarter-living?ref=discovery',
    'https://www.kickstarter.com/projects/476090608/the-good-life?ref=discovery',
    'https://www.kickstarter.com/projects/mxpx/mxpx-full-length-album-10?ref=discovery',
    'https://www.kickstarter.com/projects/earjellies/earjellies-ear-plugs?ref=discovery',
    'https://www.kickstarter.com/projects/stoneuk/stone-the-chefs-notebook?ref=discovery',
    'https://www.kickstarter.com/projects/iacollaborative/kelvin-home-coffee-roaster?ref=discovery',
    'https://www.kickstarter.com/projects/424958948/revol-dog-crate-snooz-pad-a-dog-crate-revolution?ref=discovery']


def discover(**params):
    return generate_url(req_data=params, base=base)


def search(driver):
    url = discover(staff_picks=1, sort='popularity', seed=2537785, page=1)
    print('request..')
    driver.get(url)
    hrefs = []
    elements = driver.driver.find_elements_by_class_name('hover-text-underline')
    for element in elements:
        href = element.get_property('href')
        if '.com/projects/' in href:
            hrefs.append(href)

    print(hrefs)


if __name__ == '__main__':
    print('loading...')
    driver = WebDriver('chrome-headless').driver
    wait = ui.WebDriverWait(driver, 10)

    # hrefs = search(driver)
    hrefs = collected_hrefs

    for href in hrefs:
        print(href)

        print('request..')
        driver.get(href)
        wait.until(lambda driver: driver.find_element_by_css_selector(
            "[class='block type-16 type-24-md medium navy-700 js-num']"))

        print('collecting data.')
        title = driver.find_element_by_css_selector(
            "[class='type-24 type-28-sm type-38-md navy-700 medium mb3']").text
        info = driver.find_element_by_css_selector("[class='type-14 type-18-md navy-600 mb0']").text
        funded = driver.find_element_by_css_selector(
            "[class='green-700 inline-block js-convert_pledged medium type-16 type-24-md']").text
        goal = driver.find_element_by_css_selector("[class='money']").text
        backers = driver.find_element_by_css_selector(
            "[class='js-backers_count block type-16 type-24-md medium navy-700']").text
        days = driver.find_element_by_css_selector("[class='block type-16 type-24-md medium navy-700 js-num']").text
        total = {'title': title, 'info': info, 'funded': funded, 'goal': goal, 'backers': backers, 'days': days}
        data = json.dumps(total)

        print(data)
        with open('save.txt', 'a+') as f:
            f.write(data + '\n')
