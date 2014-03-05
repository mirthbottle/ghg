# try scraping
# import requests
# from requests.auth import HTTPBasicAuth

from selenium import webdriver


browser = webdriver.Firefox()
browser.get("https://www.cdp.net/en-US/MyCDP/Anonymous/Login.aspx") # get link later
raw_input('enter after logging in')
browser.get("https://www.cdp.net/en-US/Results/Pages/More-Search-Term-By-Organization-Name.aspx?Search=True&Programme=1&Year=2013&ReportingStatus=1&Country=USA")

def get_footprint_per_page(browser):
    links = browser.find_elements_by_link_text("2013 - View Climate Change (Investor ) Response")
    for s in links:
        s.click()
        browser.switch_to_window(browser.window_handles[1])
        get_footprint_per_company(browser)

def get_footprint_per_company(browser):
    company_name = t.lstrip("- Carbon Disclosure ProjectInvestor CDP 2013 Information Request - ")
    temp1 = browser.page_source.split('Please provide your gross global Scope 1 emissions figures in metric tonnes CO2e')[1].lstrip('</strong></div></div></div></span></h4><div class="cdp-question-body"><p class="cdp-question-body-text">')
    scope_1_total = temp1[0:20].split('</p>')[0]
    temp2 = temp1.split('Please provide your gross global Scope 2 emissions figures in metric tonnes CO2e')[1].split('<p class="cdp-question-body-text">')[1].lstrip('<p class="cdp-question-body-text">')
    scope_2_total = temp2[0:20].split('</p>')[0]
    # get scope 3 table
    temp3 = temp1.split('Please account for your organization')[1].split('<table')[1].split('</table>')[0]
    # parse values from table
    
# go to pg 2
link = browser.find_element_by_link_text("2")

browser.get("https://www.cdp.net/sites/2013/04/304/Investor%20CDP%202013/Pages/DisclosureView.aspx")

browser.title # has the name of the corporation
browser.page_source



# open(filename, mode)

# reports in metric tons
# page 8 q2 scope1 emissions total 
# page 8 q3 scope2 emissions total
# page 14 q1 table of all scope3 categories and amounts 

# click all links to reports - View  Climate Change (Investor ) Response

