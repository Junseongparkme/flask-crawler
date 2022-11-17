from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
  base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
  response = get(f"{base_url}{keyword}")
  
  if response.status_code != 200:
    print("Can't request website")
  else:
    results = []
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("section", {"class": "jobs"})
    for job_section in jobs:
      job_posts = job_section.find_all("li", {"class": "feature"})
      for post in job_posts:
        anchor = post.find_all('a')[1]
        link = anchor['href']
        title = anchor.find("span", {"class" : "title"})
        company, position, region = anchor.find_all("span", {"class" : "company"})
        job_data = {
          "Link": f"https://weworkremotely.com/{link}",
          "Company": company.string.replace(",", " "),
          "Position": position.string.replace(",", " "),
          "Location": region.string.replace(",", " ")
        }
        results.append(job_data)
  return results