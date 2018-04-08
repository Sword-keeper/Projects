from Spiders.tools import generate_url, get_page, WebDriver

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
    driver = WebDriver()

    # hrefs = search(driver)
    hrefs = collected_hrefs

    for href in hrefs:
        print(href)
        print('request..')
        driver.get(href)

        print('finding title.')
        title = driver.driver.find_element_by_css_selector("[class='type-14 type-18-md navy-600 mb0']").text
        print(title)