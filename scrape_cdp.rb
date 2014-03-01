# use mechanize
require 'mechanize'

# select dropdown menu for Year (2013)
# select Reporting Status (Answered Questionnaire)
# select Country (USA)
# ~480 records

# reports in metric tons
# page 8 q2 scope1 emissions total 
# page 8 q3 scope2 emissions total
# page 14 q1 table of all scope3 categories and amounts 

# click all links to reports - View  Climate Change (Investor ) Response

agent = Mechanize.new
login_page = agent.get("https://www.cdp.net/en-US/MyCDP/Anonymous/Login.aspx")

page = agent.get('https://www.cdp.net/en-US/Results/Pages/More-Search-Term-By-Organization-Name.aspx?Search=True&Programme=1&Year=2013&ReportingStatus=1&Country=USA')


puts page.title

agent.add_auth('https://www.cdp.net/',"mirthbottle@gmail.com",'h4rh4rh4r*')
aes = agent.get('https://www.cdp.net/sites/2013/04/304/Investor%20CDP%202013/Pages/DisclosureView.aspx')
puts aes.body





