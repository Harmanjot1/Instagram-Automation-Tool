import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time 

# Imports to save posts to computer
import os
import wget

# Path to ChromeDriver
PATH = "C:\Program Files (x86)\Chrome Driver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

#d
# time.sleep() is used to sleep the system while next webpage's html loads
def login(username, password):

	driver.get("https://www.instagram.com/")

	# Accept broswer cookies pop up message
	if driver.find_element_by_xpath("//button[normalize-space()='Accept All']").size != 0: # Checking of pop-up message exists
		cookies = driver.find_element_by_xpath("//button[normalize-space()='Accept All']") # if exists then Accept cookies xpath
		cookies.send_keys(Keys.RETURN) # press enter on xpath
		time.sleep(1)

	#Login
	driver.find_element_by_xpath("//input[@name='username']").send_keys(username) # Login: Username input xpath
	time.sleep(1)
	driver.find_element_by_xpath("//input[@name='password']").send_keys(password,Keys.RETURN) # Login: Password input xpath
	time.sleep(3)

	# Notification pop-up window (Similar concept applied when compared to browser cookies pop-up)
	if driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').size != 0:
		driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').send_keys(Keys.RETURN)

# Function used to like and comment on instagram posts
def follow(webpage,commentInput):
	driver.get(webpage) # webpage to visit

	followers = driver.find_element_by_xpath("//a[contains(.,'followers')]/span").get_attribute("title") # gets number of followers on the page

	print(followers) # prints followers

	time.sleep(2)

	# lists to store post links to vists
	links = [] # used to store every <a> link on the webpage
	true_link = []  # used to store every link from links list that contains '.com/p/'

	links = driver.find_elements_by_tag_name('a') #  getting every link on webpage

	def condition(link):
		return '.com/p/' in link.get_attribute('href') # checking if links contains '.com/p/'

	valid_links = list(filter(condition,links)) # validating links


	for i in range(5):
		link = valid_links[i].get_attribute('href') # for every link in valid_links list, get attribute href

		if link not in links:
			true_link.append(link) # append accessable link to true_link list

	# for loop for every link inside true_links
	for i in true_link:
		driver.get(i) # visting the link page

		#Liking the post
		driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').send_keys(Keys.RETURN)

		#clicking on comment input box
		driver.find_element_by_class_name('RxpZH').click()
		time.sleep(1)
		
		#entering comment 
		driver.find_element_by_xpath("//textarea[contains(@placeholder,'Add a comment…')]").send_keys(commentInput)

		#pressing submit comment
		driver.find_element_by_xpath("//button[@type='submit']").click()
		time.sleep(1)

# used to download post images on any given webpage
def downloadImg(webpage):

	driver.get(webpage) #visting the given webpage
	n_scrolls = 2 # number of scrolls before getting every link on webpage
	# 2 scrolls cover roughly 35 posts
	#3 scrolls cover roughly 45 posts

	# scrolling down the page for n_scrolls times
	for i in range(0,n_scrolls):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(5)

	#getting every link on webpage
	posts = driver.find_elements_by_tag_name('a')
	posts = [a.get_attribute('href') for a in posts] #getting every href link attrubite from posts

	posts = [a for a in posts if str(a).startswith("https://www.instagram.com/p/")] #list comprehension on posts for all links staring with "https://www.instagram.com/p/"

	images = [] # list to store images

	# for loop to iterate through posts and get post image
	for a in posts:
		driver.get(a) # visting post
		time.sleep(2)
		img = driver.find_elements_by_tag_name('img') # getting any tag name img
		img = [i.get_attribute('src') for i in img] # getting the source of img
		images.append(img[i]) # appending image to list

	# Save to computer

	# Getting Path
	path = os.getcwd()
	path = os.path.join(path, "Downloads") #  Creating folder 

	os.mkdir(path)

	counter = 0
	for i in images:
		# saving images in the created folder
		save_as = os.path.join(path,"InstagramDownload"+ str(counter)+'.jpg')
		wget.download(i, save_as)
		counter += 1


if __name__ == "__main__":

	# User information
	time.sleep(5)
	
	# comment to input 
	# can also be changed to a list to have variety of comments 
	commentInput = "Nice Car"

	# user options for login information
	print("Login information")
	user = input("Press 1 : User pre-defined Username and Password \nPress 2 : Give your own Username and Password \n")

	if user == "1": 
		username = "harmanjotss27@gmail.com"
		password = "Singhsekhon1"
	elif user == "2":
		username = input("Please enter your username")
		password = input("Please enter your password")
	else:
		print("Incorrect input.")

	# user options for what webpage to visit
	print("Webpage to visit:")
	webpageinput = input("Press 1 to use pre-defined webpage \nPress 2 to input specific webpage. \n")

	if webpageinput == "1":
		webpage = "https://www.instagram.com/mercedesbenz/"
	elif webpageinput == "2":
		webpage = input("Please enter webpage in the given format 'https://www.instagram.com/mercedesbenz/'. \n")


	# user options for action this tool must take
	print("Would you like to like and comment or download post images?")

	action = input("Press 1 for like and comment \nPress 2 for download post images \nPress 3 for like, comment and download. \n")

	if action == "1":
		login(username,password)
		follow(webpage,commentInput)
	elif action == "2":
		login(username,password)
		download(webpage)
	elif action == "3":
		login(username,password)
		follow(webpage,commentInput)
		time.sleep(10)
		download(webpage)
	else:
		print("Incorrect action.")