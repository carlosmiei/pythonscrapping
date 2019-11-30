from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time,csv,sys


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")



def create_csv(save_csv,name):
    with open("finalResult"+ name +".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(['Firm Name','Country','Date','Report'])
        writer.writerows(save_csv)
        print('Final CSV of '+name +' created!')

def scrap_page(url):
    print('Starting scrapping, please wait! This may take several minutes depending on response time of the server and the quantity to parse.')
    final = []
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
    driver.get(url)
    while True:
        try:
            elm = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='button-1 button-wide']")))
            elm.click()
        except:
            break

    els = driver.find_elements_by_xpath("//*[@class='ccc-item']")

    for element in els:
        itemdesc = element.find_element_by_class_name("ccc-item-desc")
        name = itemdesc.find_element_by_css_selector('a').text
        meta = itemdesc.find_elements_by_class_name("ccc-item-meta")
        country = meta[0].text
        country = country.split(':')
        country = country[1]
        date = meta[1].text
        date = date.split(':')
        date = date[1]
        download = element.find_element_by_class_name("ccc-item-controls")
        download = download.find_element_by_css_selector('a').get_attribute('href')
        tmp = [name,country,date,download]
        final.append(tmp)
    return final


def main():
    decisions = 'https://pcaobus.org/Enforcement/Decisions/Pages/default.aspx'
    reports = 'https://pcaobus.org/Inspections/Reports/Pages/default.aspx'
    info=[]

    if (len(sys.argv)>1):
        filename = sys.argv[1]
        
        if filename == 'Decisions':
            info = scrap_page(decisions)

        if filename == 'Reports':
            info = scrap_page(reports)
        else:
            print('Wrong argument! Choose: Decisions or Reports')

        create_csv(info,filename)

    else:
        print('Missing argument! Choose: Decisions or Reports')


main()
    
