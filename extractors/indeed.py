from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# Repl.it에서 Selenium을 실행시키기 위한 설정
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(options = options)

def get_page_count(keyword):
  base_url = "https://www.indeed.com/jobs?q="
  browser.get(f"{base_url}{keyword}")
  soup = BeautifulSoup(browser.page_source, "html.parser")
  pagination = soup.find("nav", {"aria-label": "pagination"})

  pages = pagination.find_all("div", recursive=False)
  count = len(pages)

  if count >= 5:
    return 5
  elif count == 0:
    return 1
  else:
    return count

def extract_indeed_jobs(keyword):
  results = []
  pages = get_page_count(keyword)
  
  for page in range(pages):
    base_url = "https://www.indeed.com/jobs?q="
    browser.get(f"{base_url}{keyword}&start={page * 10}")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    job_list = soup.find("ul", {"class": "jobsearch-ResultsList"})
    jobs = job_list.find_all("li", recursive=False)
    
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find("span", {"class": "companyName"})
        location = job.find("div", {"class": "companyLocation"})

        job_data = {
          "Link": f"https://www.indeed.com{link}",
          "Company": company.string.replace(",", " "),
          "Position": title.replace(",", " ")
        }
          
        if location.string != None:
          job_data["Location"] = location.string.replace(",", " ")
        else:
          job_data["Location"] = "Unknown"

        results.append(job_data)
  return results