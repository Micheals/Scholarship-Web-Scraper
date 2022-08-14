# TODO if deadline has past then remove old entry from file
# TODO set script to run a schedule

import re
import csv
import requests
import webbrowser
from bs4 import BeautifulSoup

base_url = 'https://www.careeronestop.org/Toolkit/Training/find-scholarships.aspx'

# website headers
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 '
                  'Safari/537.36 '
}

all_scholarships = requests.get(f"{base_url}?&curPage=1&pagesize={8722}", headers=headers).text

soup = BeautifulSoup(all_scholarships, 'html.parser')

# Print purposes
# for i in soup.find_all(text=re.compile('Purposes:')):
#     print(i.strip())

scholarship_table = soup.find('table', class_='cos-table-responsive')

with open('careeronestop-results.csv', 'w', encoding='utf-8') as file:
    # t_headers = ['Award Name', 'Organization', 'Purposes', 'Level Of Study', 'Award Type', 'Award Amount', 'Deadline']
    # writer = csv.writer(file, fieldnames=t_headers)
    # writer.writeheader()
    file.write('Award Name|Organization|Purposes|Level Of Study|Award Type|Award Amount|Deadline|Url\n')
    for body in scholarship_table.find_all('tbody'):
        for row in body.find_all('tr'):
            for data in row.find_all('td', headers='thAN'):
                for i, k in zip(data.find_all('div', class_="notranslate detailPageLink"),
                                data.find_all(text=re.compile('Purposes:'))):
                    award_name = i.find_next().text.strip()
                    organization = i.find_next().find_next().find_next().text.strip()
                    purpose = k.strip().split(':')[1].strip()
                    if purpose == '':
                        purpose = 'Unable to scrape purpose. Please read the purpose by clicking the link!'

                for los in row.find_all('td', headers='thLOS'):
                    level_of_study = los.text.strip()

                for at in row.find_all('td', headers='thAT'):
                    award_type = at.text.strip()

                for aa in row.find_all('td', headers='thAA'):
                    award_amount = aa.text.strip()

                for d in row.find_all('td', headers='thD'):
                    deadline = d.text.strip()
                    if deadline == '':
                        deadline = "No Deadline Specified"

            url = 'www.careeronestop.org/' + row.find('a', title='Click here for detail information').get('href')
            # print('https://www.careeronestop.org/' + url)
            # print("-----------------------------------------------------------------------------------------")

            file.write(
                f"{award_name}|{organization}|{purpose}|{level_of_study}|{award_type}|{award_amount}|{deadline}|{url}\n")

        # title = row.find('div', class_='notranslate')
        # print(title.text.strip())
        # print(url.get('href'))
