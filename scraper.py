import requests
import re
from bs4 import BeautifulSoup

url = "https://www.ycombinator.com/jobs"
response =  requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

print(f"Recevied a response code of {response.status_code}")

jobs = []

job_listings = soup.find_all("div", class_ = "flex flex-col items-start gap-y-1 md:gap-y-0 md:text-left")

for job in job_listings:
    company_data = job.find("a", class_ = "hidden justify-start leading-loose md:block")
    company_name = company_data.find("span", class_ = "block font-bold md:inline").text.strip()
    company_or_job_description = company_data.find("span", class_ = "text-gray-700 md:mr-2").text.strip()

    try: 
        information_block =  job.find("div", class_ = "flex flex-wrap items-center gap-x-1 text-sm md:text-base").text.strip().split("•")
        job_title =  information_block[0]
        job_field = information_block[1]
        job_type = information_block[2]
        if "$" in information_block[3]:
            job_salary = information_block[3]
            job_location = information_block[4]

            job_salary_integer = re.findall(r'\d+', job_salary)
            job_salary_integer = [int(num) for num in job_salary_integer]
            average_salary = (sum(job_salary_integer))/2
        else:
            print(f"{company_name} had no attached salary range")
            job_salary = "No Salaray Specified"
            job_location = information_block[3]
            average_salary = -1
    except IndexError as e:
        print(f"There was an error parsing through the data for the information block:\n{information_block}")
        print(f"Error: {e}")
    
    job_link_data = job.find("a", class_ = "text-sm font-semibold leading-tight text-linkColor md:text-base md:leading-normal")["href"]
    job_link_data = "https://www.ycombinator.com" + job_link_data





    job_data = {
        "company_name": company_name,
        "description": company_or_job_description,
        "job_title": job_title,
        "job_field": job_field,
        "job_type": job_type,
        "job_salary": job_salary,
        "average_salary": average_salary,
        "job_location": job_location,
        "job_page_link": job_link_data
    }
    
    jobs.append(job_data)

print(jobs)
