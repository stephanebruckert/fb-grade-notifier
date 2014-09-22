from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PyDbLite import Base
from facepy import *
import time
import winsound
import getpass

db = Base('grades.db')
db.create('grade', 'course', mode='open')

graph = GraphAPI("my_facebook_api_key")

username = raw_input("Username: ")
password = getpass.getpass("Password: ")

while True:
	driver = webdriver.PhantomJS('C:\phantomjs-1.9.7-windows\phantomjs.exe')
	try:
		driver.get("http://ent.unr-runn.fr/uPortal/")
		select = Select(driver.find_element_by_name('user_idp'))
		select.select_by_visible_text('ENSICAEN')
		driver.find_element_by_id('IdPList').submit()

		driver.find_element_by_id('username').send_keys(username)
		driver.find_element_by_id('password').send_keys(password)
		driver.find_element_by_id('fm1').submit()

		driver.find_element_by_id('tabLink_u1240l1s214').click()
		driver.find_element_by_id('formMenu:linknotes1').click()
		driver.find_element_by_id('_id137Pluto_108_u1240l1n228_50520_:tabledip:0:_id158Pluto_108_u1240l1n228_50520_').click()
		page = driver.find_element_by_id('_id111Pluto_108_u1240l1n228_50520_:tableel:tbody_element')

		i = 0
		for item in page.text.splitlines( ):
			if item.endswith('20'):
				line = item.split(' ',1)[1].lstrip()
				note = line.rsplit(' ', 1)[1]
				field = line.rsplit(' ', 1)[0]
				courseindb = db("course")==field
				if (len(courseindb) == 0):
					db.insert(grade=note, course=field)
					graph.post(path='486181564779150/feed/', message='Nouvelle note : ' + field)
					db.commit()
					Freq = 2500 # Set Frequency To 2500 Hertz
					Dur = 1000 # Set Duration To 1000 ms == 1 second
					winsound.Beep(Freq,Dur)
					print "A new grade is available " + field + " : " + note
					
				else:
					for rec in courseindb: #only one
						if (rec["grade"] != note):
							#FB update
							Freq = 2500 # Set Frequency To 2500 Hertz
							Dur = 1000 # Set Duration To 1000 ms == 1 second
							winsound.Beep(Freq,Dur)
							print "A grade has just been updated for " + field + " : " + note 
				i+=1

		print "Successfully retrieved", i, "grades."
	except:
		print "Timed out. Trying again..."
	finally:
		driver.close()
		
	print "Waiting..."
	time.sleep(20)