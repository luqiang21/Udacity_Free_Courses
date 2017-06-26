import requests
from bs4 import BeautifulSoup
from carriers import *
from airports import *

html_page = "options.html"

carriers = extract_carriers(html_page)
airports = extract_airports(html_page)
print carriers, airports
print len(carriers), len(airports)

for carrier in carriers[:3]:

    s = requests.Session()

    r = s.get("https://www.transtats.bts.gov/Data_Elements.aspx?Data=2")
    soup = BeautifulSoup(r.text,"lxml")
    viewstate_element = soup.find(id="__VIEWSTATE")
    viewstate = viewstate_element['value']
    eventvalidation_element = soup.find(id="__EVENTVALIDATION")
    eventvalidation = eventvalidation_element["value"]

    viewstategenerator_element = soup.find(id="__VIEWSTATEGENERATOR")
    viewstategenerator = viewstategenerator_element["value"]

    r = s.post("https://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
               data = (
                       ("__EVENTTARGET", ""),
                       ("__EVENTARGUMENT", ""),
                       ("__VIEWSTATE", viewstate),
                       ("__VIEWSTATEGENERATOR",viewstategenerator),
                       ("__EVENTVALIDATION", eventvalidation),
                       ("CarrierList", "VX"),
                       ("AirportList", "BOS"),
                       ("Submit", "Submit")
                      ))
    # carrier = carriers[1]
    airport = airports[carriers.index(carrier)]
    f = open("data/"+carrier+'-'+airport+".html", "w")
    f.write(r.text)
