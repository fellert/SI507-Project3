# Ethan Ellert
# SI507


from bs4 import BeautifulSoup
import unittest
import requests
import csv

## NOTE OF ADVICE:
# When you go to make your GitHub milestones, think pretty seriously about
# all the different parts and their requirements, and what you need to
# understand. Make sure you've asked your questions about Part 2 as much
# as you need to before Fall Break!


######### PART 0 #########

part0 = requests.get("http://newmantaylor.com/gallery.html")
soup = BeautifulSoup(part0.content, 'html.parser')

images = soup.find_all('img')
for i in images:
    print(i.get('alt', 'No alternative text provided!'))


######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

try:
  parks_data = open("nps_gov_data.html",'r').read()
except:
  parks_data = requests.get("https://www.nps.gov/index.htm").text
  f = open("nps_gov_data.html",'w')
  # Cahces data in file for later use
  f.write(parks_data)
  f.close()

# Get individual states' data...

# Result of a following try/except block should be three html files
#   arkansas_data.html
#   california_data.html
#   michigan_data.html

# Stores the states we are targeting - for compiling links and doc names
states_interested = {'ar': 'arkansas', 'ca': 'california', 'mi': 'michigan'}

# Create a BeautifulSoup instance of main page data
gov_soup = BeautifulSoup(parks_data, 'html.parser')

try: # tries to open files, if they exist
    arkansas = open('arkansas_data.html', 'r').read()
    california = open('california_data.html', 'r').read()
    michigan = open('michigan_data.html', 'r').read()
except:
    ul = gov_soup.find('ul', class_='dropdown-menu') # access dropdown menu
    for li in ul.find_all('li'): # iterates through list of all 'li' elements
        url = ''
        a = li.find('a')
        href = a['href'] # Gets the href element of 'a'
        for key in states_interested:
            if key in href: # if the state matches the ones we want
                url = 'https://www.nps.gov' + href # Concatenates link
                state_data = requests.get(url).text
                f = open(states_interested[key] + '_data.html', 'w')
                # write each set of data to a file so this
                # won't have to run again.
                f.write(state_data)
                f.close()
    arkansas = open('arkansas_data.html', 'r').read()
    california = open('california_data.html', 'r').read()
    michigan = open('michigan_data.html', 'r').read()


######### PART 2 #########

# Creates BeautifulSoup instance for each of the three states
arkansas_soup = BeautifulSoup(arkansas, 'html.parser')
california_soup = BeautifulSoup(california, 'html.parser')
michigan_soup = BeautifulSoup(michigan, 'html.parser')


## Define your class NationalSite here:

class NationalSite(object):

    def __init__(self, soup):
        self.soup = soup
        self.location = self.soup.h4.text
        self.name = self.soup.h3.text
        self.type = self.soup.h2.text
        self.description = self.soup.p.text.strip('\n')

    def __str__(self):
        return '%s | %s' % (self.name, self.location)

    def __contains__(self, txt):
        return txt in str(self.name)

    def get_mailing_address(self):
        url = self.soup.find_all('a')[2]["href"]
        content = requests.get(url).text
        ad = BeautifulSoup(content, 'html.parser')
        string_list = []
        string = ''
        address = ad.find('p', class_='adr').text.strip()
        # replaces sections with multiple newlines - otherwise /// is returned
        address = address.replace('\n\n\n', ' / ')
        address = address.replace('\n', ' / ')
        return address


# Recommendation: to test the class, at various points, uncomment the
# following code and invoke some of the methods / check out the instance
# variables of the test instance saved in the variable sample_inst:

#f = open("sample_html_of_park.html",'r')
#soup_park_inst = BeautifulSoup(f.read(), 'html.parser')
#sample_inst = NationalSite(soup_park_inst)
#f.close()


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

arkansas_natl_sites = []
california_natl_sites = []
michigan_natl_sites = []

# Finds all of the park sites on each state page. These are all list elements
# inside and have a class of 'clearfix'. There is one <li> at the very end
# that also contains this class label, which is why it is excluded in the
# if statement

for x in arkansas_soup.find_all('li', class_='clearfix'):
    if 'numbers_download' not in str(x):
        site = BeautifulSoup(str(x), 'html.parser')
        arkansas_natl_sites.append(NationalSite(site))

for x in california_soup.find_all('li', class_='clearfix'):
    if 'numbers_download' not in str(x):
        site = BeautifulSoup(str(x), 'html.parser')
        california_natl_sites.append(NationalSite(site))

for x in michigan_soup.find_all('li', class_='clearfix'):
    if 'numbers_download' not in str(x):
        site = BeautifulSoup(str(x), 'html.parser')
        michigan_natl_sites.append(NationalSite(site))


#Code to help you test these out:
#for p in california_natl_sites:
# 	print(p)
#for a in arkansas_natl_sites:
# 	print(a)
#for m in michigan_natl_sites:
#    print(m)

######### PART 4 #########


# Creates three CSV files to store NationalSite data. Inputs 'None' if the
# particular element == None

with open("arkansas.csv", "w") as arkansas_csv:
    writer = csv.writer(arkansas_csv,delimiter=',')
    writer.writerow(["Name", "Location", "Type", "Address", "Description"])
    for site in arkansas_natl_sites:
        writer.writerow([site.name, site.location or 'None',
                         site.type or 'None', site.get_mailing_address(),
                         site.description])


with open("california.csv", "w") as california_csv:
    writer = csv.writer(california_csv,delimiter=',')
    writer.writerow(["Name", "Location", "Type", "Address", "Description"])
    for site in california_natl_sites:
        writer.writerow([site.name, site.location or 'None',
                         site.type or 'None', site.get_mailing_address(),
                         site.description])

with open("michigan.csv", "w") as michigan_csv:
    writer = csv.writer(michigan_csv,delimiter=',')
    writer.writerow(["Name", "Location", "Type", "Address", "Description"])
    for site in michigan_natl_sites:
        writer.writerow([site.name, site.location or 'None',
                         site.type or 'None', site.get_mailing_address(),
                         site.description])
