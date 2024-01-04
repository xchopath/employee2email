#!/usr/bin/env python3

from linkedin_scraper import Company, actions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

company_linkedin = "https://www.linkedin.com/company/google"
organization_domain = 'google.com'
email = "<your-linkedin-email>"
password = "<password>"

def emailGenerate(employeename, domain):
	try:
		dicts = employeename.lower().split(" ")
		if len(dicts) > 1:
			firstname = dicts[0]
			dicts.pop(0)
			emails = []
			separators = ['', '.']
			for guessname in dicts:
				for separator in separators:
					email = firstname + str(separator) + guessname + '@' + domain
					if email not in emails:
						emails.append(email)
			return emails
	except Exception:
		return

driver = webdriver.Chrome()
actions.login(driver, email, password)
wait = WebDriverWait(driver, 10)
driver.get(company_linkedin + "/people/")

employees = []
for _ in range(10):
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "org-people-profile-card__profile-title")))
	for element in elements:
		if element.text not in employees:
			employees.append(element.text)
	time.sleep(1)

for employee in employees:
	try:
		mail_list = emailGenerate(employee, organization_domain)
		for email in mail_list:
			print(email)
	except:
		continue
