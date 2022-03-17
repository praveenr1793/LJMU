from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import Restarted
import pandas as pd
import json
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


ZomatoData = pd.read_csv('zomato.csv')
ZomatoData = ZomatoData.drop_duplicates().reset_index(drop=True)
WeOperate = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai', 'Ranchi', 'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara', 'Dehradun', 'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad', 'Coimbatore', 'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal', 'Goa', 'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla']

import socket
socket.getaddrinfo('localhost', 8080)

def RestaurantSearch(City,Cuisine):
	TEMP = ZomatoData[(ZomatoData['Cuisines'].apply(lambda x: Cuisine.lower() in x.lower())) & (ZomatoData['City'].apply(lambda x: City.lower() in x.lower()))]
	return TEMP[['Restaurant Name','Address','Average Cost for two','Aggregate rating']]

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_search_restaurants'

	def run(self, dispatcher, tracker, domain):
		
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		price = tracker.get_slot('price')

		results = RestaurantSearch(City=loc,Cuisine=cuisine)
		results = pd.DataFrame(results)

		response=""
		if(price=="low"):
			filterd_results = results[results['Average Cost for two'] <=300]
			filterd_results.sort_values('Aggregate rating',ascending=False,inplace=True)
			if(len(filterd_results)==0):
				#SlotSet("price", None)
				dispatcher.utter_message("Sorry we couldn't find any restaurants in the mentioned price range. Please choose different budget")
				return[SlotSet("price", None)]
				#return[SlotSet("query_restaurant_search", None)]
				#response=response+" Sorry couldn't find any restaurants in price range. Please re enter different price range "
			else:
				for index, row in filterd_results.head(5).iterrows():
					response = response+row['Restaurant Name']+" in "+ row['Address']+" has been rated "+str(row['Aggregate rating'])+"\n"
				dispatcher.utter_message(response)
	
				return[SlotSet("price", price)]
				#return[SlotSet("query_restaurant_search", response)]
		elif(price=="mid"):
			filterd_results = results[(results['Average Cost for two'] > 300) &  (results['Average Cost for two'] <= 700)]
			filterd_results.sort_values('Aggregate rating',ascending=False,inplace=True)
			if(len(filterd_results)==0):
				#SlotSet("price", None)
				dispatcher.utter_message("Sorry we couldn't find any restaurants in the mentioned price range. Please choose different budget")
				return[SlotSet("price", None)]
				#return[SlotSet("query_restaurant_search", None)]
			else:
				for index, row in filterd_results.head(5).iterrows():
					response = response+row['Restaurant Name']+" in "+ row['Address']+" has been rated "+str(row['Aggregate rating'])+"\n"
				dispatcher.utter_message(response)
				return[SlotSet("price", price)]
				#return[SlotSet("query_restaurant_search", response)]
		elif(price=="high"):				
			filterd_results = results[results['Average Cost for two'] >700]
			filterd_results.sort_values('Aggregate rating',ascending=False,inplace=True)
			if(len(filterd_results)==0):
				#response=response+" Sorry couldn't find any restaurants in price range. Please re enter different price range "
				#SlotSet("price", None)
				dispatcher.utter_message("Sorry we couldn't find any restaurants in the mentioned price range. Please choose different budget")
				return[SlotSet("price", None)]
				#return[SlotSet("query_restaurant_search", None)]
			else:
				for index, row in filterd_results.head(5).iterrows():
					response = response+row['Restaurant Name']+" in "+ row['Address']+" has been rated "+str(row['Aggregate rating'])+"\n"	
				dispatcher.utter_message(response)
				return[SlotSet("price", price)]
				#return[SlotSet("query_restaurant_search", response)]



class ActionValidateLocation(Action):
	def name(self):
		return 'action_validate_location'
		
	def run(self, dispatcher, tracker, domain):
		city_list = ['ahmedabad', 'bangalore', 'chennai', 'delhi', 'hyderabad', 'kolkata', 'mumbai', 'pune',
					'agra', 'ajmer', 'aligarh', 'allahabad', 'amravati', 'amritsar', 'asansol', 'aurangabad', 'bareilly', 'belgaum', 
					'bhavnagar', 'bhiwandi', 'bhopal', 'bhubaneswar', 'bikaner', 'bokaro steel city', 'chandigarh', 'coimbatore', 
					 'cuttack', 'dehradun', 'dhanbad', 'durg-bhilai nagar', 'durgapur', 'erode', 'faridabad', 'firozabad', 'ghaziabad', 
					 'gorakhpur', 'gulbarga', 'guntur', 'gurgaon', 'guwahati', 'gwalior', 'hubli-dharwad', 'indore', 'jabalpur', 'jaipur', 
					 'jalandhar', 'jammu', 'jamnagar', 'jamshedpur', 'jhansi', 'jodhpur', 'kannur', 'kanpur', 'kakinada', 'kochi', 'kottayam', 
					 'kolhapur', 'kollam', 'kota', 'kozhikode', 'kurnool', 'lucknow', 'ludhiana', 'madurai', 'malappuram', 'mathura', 'goa', 
					 'mangalore', 'meerut', 'moradabad', 'mysore', 'nagpur', 'nanded', 'nashik', 'nellore', 'noida', 'palakkad', 'patna', 
					 'pondicherry', 'raipur', 'rajkot', 'rajahmundry', 'ranchi', 'rourkela', 'salem', 'sangli', 'siliguri', 'solapur', 
					 'srinagar', 'sultanpur', 'surat', 'thiruvananthapuram', 'thrissur', 'tiruchirappalli', 'tirunelveli', 'tiruppur', 
					 'ujjain', 'vijayapura', 'vadodara', 'varanasi', 'vasai-virar city', 'vijayawada', 'visakhapatnam', 'warangal']
		loc = tracker.get_slot('location')
		response = ""
		if(loc == None):
			dispatcher.utter_template("utter_ask_location",tracker)
			return [SlotSet('location',None)]
		elif(loc.lower() not in city_list):
			dispatcher.utter_template("utter_location_invalid",tracker)
			return [SlotSet('location',None)]
		else:
			return [SlotSet('location',loc)]

class ActionValidateCuisine(Action):
	def name(self):
		return 'action_validate_cuisine'
	
	def run(self, dispatcher, tracker, domain):
		cuisines=['mexican','chinese','italian','american','north indian','south indian']
		cuisine = tracker.get_slot('cuisine')
		#response = ""
		if(cuisine == None):
			dispatcher.utter_template("utter_ask_cuisine",tracker)
			return [SlotSet('cuisine',None)]
		elif(cuisine.lower() not in cuisines):
			dispatcher.utter_template("utter_invalid_cuisine",tracker)
			return [SlotSet('cuisine',None)]
		else:
			return [SlotSet('cuisine',cuisine)]


class ActionValidatePrice(Action):
	def name(self):
		return 'action_validate_price'
	
	def run(self, dispatcher, tracker, domain):
		budget=["low","mid","high"]
		price = tracker.get_slot('price')
		dispatcher.utter_message(price)
		#response = ""
		if(price == None):
			#dispatcher.utter_template("utter_ask_budget",tracker)
			dispatcher.utter_message("We are not aware of budget, please do let us know your desired budget")
			return [SlotSet('price',None)]
		elif(price.lower() not in budget):
			#dispatcher.utter_template("utter_price_invalid",tracker)
			dispatcher.utter_message("Sorry we dont have this budget for now, try a different budget range")
			return [SlotSet('price',None)]
		else:
			return [SlotSet('price',price)]

class ActionSendMail(Action):
	def name(self):
		return 'action_send_mail'

	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		price = tracker.get_slot('price')

		email = tracker.get_slot('email')
		
		msg = MIMEMultipart('alternative')
			
		results = RestaurantSearch(City=loc,Cuisine=cuisine)
		results = pd.DataFrame(results)

		if(email==None):
			dispatcher.utter_template("utter_ask_email", tracker)
			return[SlotSet('email',None)]
		elif(len(results)==0):
			msg.attach(MIMEText("Sorry no results found",'html'))
		else:
			#email = list_email[0]
			if(price=="low"):
				filterd_results = results[results['Average Cost for two'] <=300]
				filterd_results.sort_values('Aggregate rating',ascending=False,inplace=True)
				if(len(filterd_results)==0):
					msg.attach(MIMEText("Sorry we couldn't find any restaurants in the mentioned price range. Please choose different budget",'html'))
				else:
					msg.attach(MIMEText(filterd_results.head(10).to_html(),'html'))
			elif(price=="mid"):
				filterd_results = results[(results['Average Cost for two'] > 300) &  (results['Average Cost for two'] <= 700)]
				filterd_results.sort_values('Aggregate rating',ascending=False,inplace=True)
				if(len(filterd_results)==0):
					msg.attach(MIMEText("Sorry we couldn't find any restaurants in the mentioned price range. Please choose different budget",'html'))
				else:
					msg.attach(MIMEText(filterd_results.head(10).to_html(),'html'))
			elif(price=="high"):				
				filterd_results = results[results['Average Cost for two'] >700]
				filterd_results.sort_values('Aggregate rating',ascending=False,inplace=True)
				if(len(filterd_results)==0):
					msg.attach(MIMEText("Sorry we couldn't find any restaurants in the mentioned price range. Please choose different budget",'html'))
				else:
					msg.attach(MIMEText(filterd_results.head(10).to_html(),'html'))

		msg['Subject'] = 'Zomato: List of Restuarants'
		msg['From'] = 'chatfobot@gmail.com'
		msg['To'] = email

			# Send the message via our own SMTP server.

			#server = smtplib.SMTP('smtp.gmail.com:587')
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
			#server.starttls()
		server.login('chatfobot@gmail.com','chatfobot2021')
		server.send_message(msg)
		server.quit()
		
		dispatcher.utter_template("utter_confirm_email", tracker)
		return[SlotSet('email',email)]			

class ActionRestarted(Action): 	
    def name(self): 		
        return 'action_restarted' 	
    def run(self, dispatcher, tracker, domain): 
        return[Restarted()]
class ActionSlotReset(Action): 	
    def name(self): 		
        return 'action_slot_reset' 	
    def run(self, dispatcher, tracker, domain): 		
        return[AllSlotsReset()]		
