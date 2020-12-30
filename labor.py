from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(executable_path="/path_to_chromedriver")
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
	
	#User will fill Recaptcha button and click submit??
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
	if profile['Q1'].upper() == "N":
		driver.find_element_by_id("G05_REFUSE_OFFER0").click()
	elif profile['Q1'].upper() == "Y": 
		driver.find_element_by_id("G05_REFUSE_OFFER1").click()
	else:
		raise Exception("Please enter 'Y' or 'N'")

	#Question 2a: Excluding earnings from self-employment, did you earn more than $504?
	if profile['Q2a'].upper() == "NA":
		driver.find_element_by_id("G05_EXCEEDED_MAX_EARNINGS3").click()
	elif profile['Q2a'].upper() == "Y": 
		driver.find_element_by_id("G05_EXCEEDED_MAX_EARNINGS1").click()
	elif profile['Q2a'].upper() == "N":
		driver.find_element_by_id("G05_EXCEEDED_MAX_EARNINGS0").click()
	else:
		raise Exception("Please enter 'Y' or 'N'")

	#Question 6: Have you retuned to work?
	if profile['Q6'].upper() == "N":
		driver.find_element_by_id("G05_RETURNED_FULL_TIME0").click()
	elif profile['Q6'].upper() == "Y": 
		driver.find_element_by_id("G05_RETURNED_FULL_TIME1").click()
	else:
		raise Exception("Please enter 'Y' or 'N'")
	
	#when the confimation page is detected, quit the driver
	# try:
	# 	WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div/div/div[4]/div/div/div/li")))
	# except:
	# 	print("Cannot locate confirmation page")
	# driver.quit()

def get_user_info():
	
	profile['username'] = input("Enter Username: ")
	profile['password'] = input("Enter Password: ")

	profile['Q1'] = input("Last week, did you refuse any job offer or referral? (Y/N) ")
	profile['Q2'] = input("How many days did you work, including self-employment, during the week ending 8/23/2020? (Enter '4' if 4 or more) ")
	profile['Q2a'] = input("Excluding earnings from self-employment, did you earn more than $504? (Y/N/NA) ")
	profile['Q3'] = input("How many days were you NOT ready, willing, and able to work? (Enter '4' if 4 or more) ")
	profile['Q4'] = input("How many days were you owed vacation pay or did you receive vacation pay? (Enter '4' if 4 or more) ")
	profile['Q5'] = input("How many days were you owed holiday pay or did you receive holiday pay? (Enter '4' if 4 or more) ")
	profile['Q6'] = input("Have you retuned to work? (Y/N) ")

	return profile




main()


