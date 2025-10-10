import requests
import re
import json
import hashlib
from datetime import datetime
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
            #print(f"{company_name} had no attached salary range")
            job_salary = "No Salary Specified"
            job_location = information_block[3]
            average_salary = -1
    except IndexError as e:
        print(f"There was an error parsing through the data for the information block:\n{information_block}")
        print(f"Error: {e}")
    
    job_link_data = job.find("a", class_ = "text-sm font-semibold leading-tight text-linkColor md:text-base md:leading-normal")["href"]
    job_link_data = "https://www.ycombinator.com" + job_link_data

    #Create a hash of the job posting for easy checking if the job has already been posted
    job_string_before_hash = job_title + job_location + str(average_salary)
    job_hash = hashlib.md5(job_string_before_hash.encode()).hexdigest()

    job_data = {
        "company_name": company_name,
        "description": company_or_job_description,
        "job_title": job_title,
        "job_field": job_field,
        "job_type": job_type,
        "job_salary": job_salary,
        "average_salary": average_salary,
        "job_location": job_location,
        "job_page_link": job_link_data,
        "job_hash": job_hash,
        "job_post_time": datetime.now().strftime("%Y-%m-%d")
    }
    
    jobs.append(job_data)

#print(jobs)

try:
    with open("jobs.json", "r", encoding='utf-8') as f:
        previously_saved_jobs = json.load(f)
except FileNotFoundError as e:
    previously_saved_jobs = []
    print(f"The file jobs.json was not able to be read\n Error: {e}")
except json.JSONDecodeError as e:
    previously_saved_jobs = []
    print(f"Error decoding the JSON.\n Error: {e}")

for i in jobs:
    append_job = True
    for j in previously_saved_jobs:
        if j["job_hash"] == i["job_hash"]:
            #print(f"{i["job_hash"]} has already been appended")
            append_job = False
    if append_job:
        previously_saved_jobs.append(i)

with open("jobs.json", "w", encoding='utf-8') as f:
    json.dump(previously_saved_jobs,f, ensure_ascii=False,indent=4)

