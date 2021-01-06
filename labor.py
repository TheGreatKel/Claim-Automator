from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pyinputplus as pyip

driver = webdriver.Chrome(executable_path="/Users/kelvenopoku/Downloads/chromedriver")
# driver = webdriver.Chrome(executable_path="/path_to_chromedrive")
profile = {}

def main():
	
	profile = get_user_info()
	login(profile['username'], profile['password'])	
	
	if navigate() == False:
		print("There is an issue getting to your benefit claim page. Have you already claimed benefits for this week?")
	else: 
		fill()

def login(username, password):
	driver.get("https://applications.labor.ny.gov/Individual/")

	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loginform:username")))
	except:
		print("cannot locate element")
	driver.find_element_by_id("loginform:username").send_keys(username)
	driver.find_element_by_id("loginform:password").send_keys(password)
	
	#Recaptcha
	time.sleep(75)

	driver.find_element_by_id("loginform:signinButton").click()

#This function navigates to the umemployment page
def navigate():
	try:
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.LINK_TEXT, "Unemployment Services"))
		)
		driver.execute_script("arguments[0].click();", element)


		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='content']/form[1]/input[10]"))
		)
		driver.execute_script("arguments[0].click();", element)
		

		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='content']/form/center/input"))
		)
		driver.execute_script("arguments[0].click();", element)


		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div/div/div[4]/div/div/form/button"))
		)
		driver.execute_script("arguments[0].click();", element)

	except:
		return False
		

# This function fills out the unemployment form.
def fill():
	try:

		#Question 2: How many days did you work, including self-employment, during the week ending 8/23/2020? (DROP DOWN)
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "G05_TOTAL_DAYS_WORKED")
		))
		Select(element).select_by_value(profile['Q2'])

		#Question 3: How many days were you NOT ready, willing, and able to work?
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "G05_DAYS_NOT_RWA")
		))
	
		Select(element).select_by_value(profile['Q3'])

		#Question 4: How many days were you owed vacation pay or did you receive vacation pay?
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "G05_VACATION_PAY_DAYS")) 
		)
		Select(element).select_by_value(profile['Q4'])

		#Question 5: How many days were you owed holiday pay or did you receive holiday pay?
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "G05_HOLIDAY_PAY_DAYS")) 
		)
		Select(element).select_by_value(profile['Q5'])
	except:
		print("Failed")
	#Question 1:  During the week ending 8/23/2020, did you refuse any job offer or referral?
	if profile['Q1'] == "No":
		driver.find_element_by_id("G05_REFUSE_OFFER0").click()
	elif profile['Q1'] == "Yes": 
		driver.find_element_by_id("G05_REFUSE_OFFER1").click()

	#Question 2a: Excluding earnings from self-employment, did you earn more than $504?
	if profile['Q2a'] == "NA":
		driver.find_element_by_id("G05_EXCEEDED_MAX_EARNINGS3").click()
	elif profile['Q2a'] == "Yes": 
		driver.find_element_by_id("G05_EXCEEDED_MAX_EARNINGS1").click()
	elif profile['Q2a'] == "No":
		driver.find_element_by_id("G05_EXCEEDED_MAX_EARNINGS0").click()
	
	#Question 6: Have you retuned to work?
	if profile['Q6'] == "No":
		driver.find_element_by_id("G05_RETURNED_FULL_TIME0").click()
	elif profile['Q6'] == "Yes": 
		driver.find_element_by_id("G05_RETURNED_FULL_TIME1").click()
	

def get_user_info():
	
	profile['username'] = pyip.inputStr("Enter Username: ")
	profile['password'] = pyip.inputStr("Enter Password: ")
	
	profile['Q1'] = pyip.inputChoice(['Yes', 'No'], prompt="Last week, did you refuse any job offer or referral? ('Yes'/'No') ")
	profile['Q2'] = pyip.inputStr("How many days did you work, including self-employment, in the last week? (Enter '4' if 4 or more) ")
	profile['Q2a'] = pyip.inputChoice(['Yes', 'No', 'NA'], prompt="Excluding earnings from self-employment, did you earn more than $504? ('Yes'/'No'/'NA') ")
	profile['Q3'] = pyip.inputStr("How many days were you NOT ready, willing, and able to work? (Enter '4' if 4 or more) ")
	profile['Q4'] = pyip.inputStr("How many days were you owed vacation pay or did you receive vacation pay? (Enter '4' if 4 or more) ")
	profile['Q5'] = pyip.inputStr("How many days were you owed holiday pay or did you receive holiday pay? (Enter '4' if 4 or more) ")
	profile['Q6'] = pyip.inputChoice(['Yes', 'No'], prompt="Have you retuned to work? ('Yes'/'No') ")
	

	return profile


main()


