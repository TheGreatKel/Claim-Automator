from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Things to do
 # 1. refactor XPATH's with ID's
 # 1.5 Testing
 # 2. User Input
 # 3. Make a demo gif of the project for github



#Set up driver and get starting website
driver = webdriver.Safari()
driver.get("https://applications.labor.ny.gov/Individual/")


def main():
	username = input("Enter your username:")
	password = input("Enter your password")
	login(username,password)

	if navigate() == False:
		print("You have already claimed benefits for this week.")
	else: 
		fill()


def get_user_info():
	username = input("Enter Username:")
	password = input("Enter Password:")

	q1 = input("During the week ending 8/23/2020, did you refuse any job offer or referral?")
	q2 = input("How many days did you work, including self-employment, during the week ending 8/23/2020?")
	q2a = input("Excluding earnings from self-employment, did you earn more than $504?")
	q3 = input("How many days were you NOT ready, willing, and able to work?")
	q4 = input("How many days were you owed vacation pay or did you receive vacation pay?")
	q5 = input("How many days were you owed holiday pay or did you receive holiday pay?")
	q6 = input("Have you retuned to work?")



def login(username, password):
	driver.find_element_by_id("USERNAME").send_keys(username)
	driver.find_element_by_id("PASSWORD").send_keys(password)
	driver.find_element_by_id("signin").click()


#This function navigates to the umemployment page
def navigate():
	try:
		element = WebDriverWait(driver, 10).until(
			# EC.presence_of_element_located((By.LINK_TEXT, "Unemployment Services"))
			EC.presence_of_element_located((By.LINK_TEXT, "Unemployment Services"))
		)
		driver.execute_script("arguments[0].click();", element)


		element = WebDriverWait(driver, 10).until(
			# EC.presence_of_element_located((By.LINK_TEXT, "Unemployment Services"))
			EC.presence_of_element_located((By.XPATH, "//*[@id='content']/form[1]/input[10]"))
		)
		driver.execute_script("arguments[0].click();", element)
		#element.click()

		element = WebDriverWait(driver, 10).until(
			# EC.presence_of_element_located((By.LINK_TEXT, "Unemployment Services"))
			EC.presence_of_element_located((By.XPATH, "//*[@id='content']/form/center/input"))
		)
		driver.execute_script("arguments[0].click();", element)


		element = WebDriverWait(driver, 10).until(
			# EC.presence_of_element_located((By.LINK_TEXT, "Unemployment Services"))
			EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div/div/div[4]/div/div/form/button"))
		)
		driver.execute_script("arguments[0].click();", element)

	except:
		return False
		

# This function fills out the unemployment form.
def fill():
	try:
	 	#Question 1:  During the week ending 8/23/2020, did you refuse any job offer or referral?
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "G05_REFUSE_OFFER0") #Option for No
		))
		driver.execute_script("arguments[0].click();", element)

		#Question 2: How many days did you work, including self-employment, during the week ending 8/23/2020? (DROP DOWN)
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "G05_TOTAL_DAYS_WORKED")
		))
		Select(element).select_by_value("0")
		

		#Question 2a: Excluding earnings from self-employment, did you earn more than $504?
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "G05_EXCEEDED_MAX_EARNINGS3") #Option for NA
		))
		driver.execute_script("arguments[0].click();", element)

		#Question 3: How many days were you NOT ready, willing, and able to work?
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "G05_DAYS_NOT_RWA")
		))
		print("I found it!")
		#Select(element).select_by_value("1")

		#Question 4: How many days were you owed vacation pay or did you receive vacation pay?
		# element = WebDriverWait(driver, 10).until(
		# 	EC.presence_of_element_located((By.ID, "G05_VACATION_PAY_DAYS")) 
		# )
		# Select(element).select_by_value("0")

		# #Question 5: How many days were you owed holiday pay or did you receive holiday pay?
		# element = WebDriverWait(driver, 10).until(
		# 	EC.presence_of_element_located((By.ID, "G05_HOLIDAY_PAY_DAYS")) 
		# )
		# Select(element).select_by_value("0")

		# #Question 6: Have you retuned to work?
		# element = WebDriverWait(driver, 10).until(
		# 	EC.presence_of_element_located((By.ID, "G05_RETURNED_FULL_TIME0")) #Option for NO
		# )
		# Select(element).select_by_value("0")
	except:
		print("Failed")


if __name__ == "__main__":
    main()

get_user_info()


