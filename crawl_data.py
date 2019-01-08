from bs4 import BeautifulSoup
from requests import session
from lxml import html
import csv
import requests
from time import sleep
import re
import argparse
import json
    
out_file = "charts_billboard.csv" 
def crawl_data(request_path):
  rows = [] 
  html = session().get(request_path).content
  soup = BeautifulSoup(html, 'lxml') 

            
  chart_table = soup.find_all(text=re.compile("Display Chart Table"))[0]
  while chart_table.name != "table":
    chart_table = chart_table.next_element
        #table = chart.find('tr')
        #for tr in table.select('tr'):
  for tr in chart_table.select('tr'):
    row = [td.text.strip() for td in tr.select('td') if td.text.strip() and td.text.strip() != '-']
    if row:
      rows.append(row)
  return rows


if __name__ == "__main__":
  request_path = "http://www.umdmusic.com/default.asp?Lang=English&Chart=D"
  scraped_data =  crawl_data(request_path)
  with open(out_file, 'w', newline='') as f:
    while True:
    #while request_path != 'http://www.umdmusic.com/default.asp?Lang=English&Chart=D&ChDate=20171111&ChMode=P':
      print("Pulling data from: " + request_path)
      html = session().get(request_path).content
      soup = BeautifulSoup(html, 'lxml') 

      prev_link = soup.find_all(href=re.compile("ChDate=\d+&ChMode=P"))
      if len(prev_link) > 0:
        request_path = prev_link[0]['href']
        request_path = "http://www.umdmusic.com/" + request_path
        sel = re.match(".*ChDate=(\d+).*", request_path)
        chart_date = sel.group(1)
        print(chart_date)
      else:
          break
      writer = csv.writer(f)
      if scraped_data:
        print ("Writing data output to file")  
        for data in scraped_data:
          writer.writerow(data)  
