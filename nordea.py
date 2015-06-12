#encoding: utf-8
from selenium import webdriver
from getpass import getpass

class Nordea():
	"""A wrapper class to login to Nordea online bank and read current account balance.
	Uses Selenium and PhantomJS to emulate browser. You need to have PIN code access,
	doesn't support keycode access for security reasons."""

	def __init__(self, userid, pin):
		"""Takes userid and PIN code as arguments."""
		self.driver = webdriver.PhantomJS("phantomjs")
		self.url = "https://solo1.nordea.fi/nsp/login"
		self.userid = userid
		self.pin = pin
		self.connected = False

	def connect(self):
		"""Loads the bank login site."""
		self.driver.get(self.url)
		# identify correct site, this should be done better, but works for now
		if self.driver.title != "Nordean verkkopankki":
			raise Exception("Unable to connect to the website.")
			return
		self.connected = True

	def login(self):
		"""Enters the supplied user id and PIN code to their respective fields and tries to log in."""
		if not self.connected:
			print "Connect first!"
		else:
			try:
				# select the pin code access
				self.driver.find_element_by_id("tabsC").find_elements_by_css_selector("a")[1].click()
				# insert userid and pincode into the form
				self.driver.find_element_by_name("userid").send_keys(self.userid)
				for i in [1, 2, 3, 4]:
					self.driver.find_element_by_name("pin"+str(i)).send_keys(self.pin[i - 1])
				# click the login button
				self.driver.find_element_by_name("commonlogin$doLightloginForFI").click()
			except selenium.common.exceptions.NoSuchElementException:
				print "Unable to locate login form."

	def get_account_balance(self, n=1):
		"""Gets the balance of the nth account (default 1) and returns it a float."""
		try:
			rows = self.driver.find_element_by_id("currentaccountsoverviewtable").find_elements_by_css_selector("tr")
			# get the balance of the first account
			balance = rows[n].find_elements_by_css_selector("td")[3].text
			# format and return
			return float(balance.replace("+", "").replace(".", "").replace(",", "."))
		except selenium.common.exceptions.NoSuchElementException:
			print "Unable to locate account balance."
			return None

	def logout(self):
		"""Clicks the logout button."""
		self.connected = False
		# click the logout button
		try:
			self.driver.find_element_by_id("log_out_button").click()
		except selenium.common.exceptions.NoSuchElementException:
				print "Unable to locate logout button."

	def __enter__(self):
		self.connect()
		self.login()
		return self

	def __exit__(self, ty, va, tb):
		self.logout()


# a small example program to demonstrate the use of the class
if __name__ == "__main__":

	with Nordea(getpass("ID: "), getpass("PIN: ")) as nrd:
		print nrd.get_account_balance()

