from bs4 import BeautifulSoup
import requests as request
from loguru import logger
import html2text
import tabula

# Save logs to file
logger.add("app.log", rotation="10 MB", level="INFO")

# Example logs
#logger.error("Failed to fetch data from Yahoo Finance.")
url='https://www.moneycontrol.com/mutual-funds/nav/hdfc-focused-30-fund-direct-plan-growth/MHD1150'


# data=request.get(url)
# soup=BeautifulSoup(data.content,'html.parser')
# logger.info("Scraping started for stock market data.")
# if data.status_code !=200:
#     logger.warning("Error while scraping!")
# else :
#     logger.info(f"Scraped success !! Link: {url} and status code: {data.status_code}")
#     title=soup.find('h1',{'class':'page_heading navdetails_heading'})
#     tables = soup.find_all(['div'], {
#     'class': ['sipreturns_table', 'returns_table']        })
#     markdown_title = html2text.html2text(str(title))
#     markdown_text = html2text.html2text(str(tables))
#     file_name=url.split('/')[-1]
#     with open(f"{file_name}.md","w",encoding='utf-8') as f :
#           f.write(markdown_title)
#           f.write(markdown_text)

url_100_='https://www.screener.in/screens/885655/top-100-stocks/'


filepath_top100=''
def top100(str:filepath_top100)-> str :
    

