'''
Module to create, format, and validate credentials used for stuffing
'''


import string
import random
import json
import sys
import logging

import httplib2
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.file import Storage

# Set up logger
logger = logging.getLogger('Chaff.Account')


class User(object): 
    def __init__(self, first_name, last_name, netid, email, password, phone,
	country):
		'''Contains fake user data generated from UserGenerator'''
		self.logger = logging.getLogger('Chaff.Account.User')
		self.logger.debug('User class instantiated')
		self.first_name = first_name
		self.last_name = last_name
		self.full_name = self.first_name + ' ' + self.last_name
		self.netid = netid
		self.password = password
		self.phone = phone
		self.country = country
		self.email = email
			


    def __str__(self):
        content = '''
Name: {0:5}{1}
NetID: {0:4}{2}
Email: {0:4}{3}
Password: {0:1}{4}
Phone: {0:4}{5}
Country: {0:2}{6}'''.format('', self.full_name, self.netid, self.email, self.password,
	self.phone, self.country)
        return content
    
            
class UserGenerator(object):           
    def __init__(self,json_file):
		'''Creates User objects. The source data must be a json file specified
			in CLI.
		'''
		self.logger = logging.getLogger('Chaff.Account.UserGenerator')
		self.logger.debug('UserGenerator class instantiated')
		self.json_file = json_file
		self.logger.debug('Loading json file {}'.format(self.json_file)) 
		try:
			with open(self.json_file) as fake_data:
				self.jdata = json.load(fake_data)
				self.logger.debug('JSON file {} sucssefully loaded'.format(self.json_file))
		except IOError:
			self.logger.error('JSON file of user data {} not found'.format(self.json_file))
			sys.stderr.write('\nERROR: JSON file of user data "{}" not found\n'.format(self.json_file))
			sys.exit(301)
		except ValueError:
			self.logger.error('"{}" does not appear to be a valid JSON file'.format(self.json_file))
			sys.stderr.write('\n"{}" does not appear to be a valid JSON file\n'.format(self.json_file))
			sys.exit(302)
			
    def _rand_fields(self, field, sub_field=''):
        '''Pull a random entry from the specified field'''
        user_data = self.jdata['results']
        user_data = random.choice(user_data)['user']
        # Attempt to pull the field data, if there's no sub_field in the JSON,
        # python throws a TypeError. We handle it and tell it to go up a level
        try:
			self.logger.debug('"{}" pulled from JSON'.format(user_data.get(field)[sub_field]))
			return user_data.get(field)[sub_field]
        except TypeError:
			self.logger.debug('"{}" pulled from JSON'.format(user_data.get(field)))
			return user_data.get(field)
			

    def _make_name(self):
		self.logger.debug('Creating a name...')
		first_name = string.capwords(self._rand_fields(field='name',
			sub_field='first'))
		last_name = string.capwords(self._rand_fields(field='name',
			sub_field='last'))
		return first_name, last_name
		    

    def _make_netid(self, first_name, last_name, email_domain):
		self.logger.debug('Creating a netid with first name: {}, last name: {}'.format(first_name, last_name))
		# If domain is example.com, use non-school based netid format
		if email_domain == '@example.com':
			netroll = str(random.randint(1,99))
			netid = '{}.{}{}'.format(first_name,last_name,netroll)
			self.logger.debug('Created NetID "{}"'.format(netid))
			return netid
		# Roll to make NetID with 2 or 3 letters
		roll = random.randint(2,3)
		if roll == 3:
			initials = '{}{}{}'.format(string.lower((first_name[0])),
								''.join(random.choice(string.ascii_lowercase)),
								string.lower(last_name[0]))
		else:
			initials = '{}{}'.format(string.lower(first_name[0]),
							string.lower(last_name[0]))
        # Roll for NetID to have 1 - 4 numbers
		roll = random.randint(1,4)
		nums = ''.join(random.choice(string.digits) for _ in range(roll))
		netid = '{}{}'.format(initials, nums)
		self.logger.debug('Created NetID "{}"'.format(netid))
		return netid

     
    def _make_email(self, netid, email_domain):
		self.logger.debug('Creating email address with netid: {}, email_domain: {}'.format(netid, email_domain))
		email_address = '{}{}'.format(netid, email_domain)
		self.logger.debug('Created email address "{}"'.format(email_address))
		return email_address
    
    
    def _jazz_password(self, password):
		'''Takes the password from json and opts to modify it.'''
        # 40% chance of making nicer password
		if random.randint(1,5) < 3:
			# Determine how many chars we add
			padding = random.randint(1,4) 
			jazz = ''.join(random.choice(string.digits + string.punctuation) for _ in range(padding))
			# 50% chance of appending or prepending jazz
			if random.randint(1,2) == 1:
				self.logger.info('Jazzing password "{}" from JSON into "{}{}"'.format(password, password,jazz))
				return '{}{}'.format(password, jazz)
			else:
				self.logger.info('Jazzing password "{}" from JSON into "{}{}"'.format(password, jazz, password))
				return '{}{}'.format(jazz, password)
		else:
			self.logger.info('Password "{}" remains unchanged from JSON'.format(password))
			return password
      
    
    def _is_valid_google_account(self, email, auth_token):
		# Shortcut for example.com domains which will always be fake
		if email.endswith('example.com'):
			self.logger.debug('Skipping auth check for email address "{}"'.format(email))
			return False
        # NOTE: This is a tweaked C&P from Google's example to use their API
        # Load the auth token, chaff_auth, and prepare it for the http object
		storage = Storage(auth_token)
		credentials = storage.get()
        # Create an httplib2.Http object and authorize it with our credentials
		http = httplib2.Http()
		try:
			http = credentials.authorize(http)
		except AttributeError as err:
			self.logger.error('ERROR: {}; check google auth token\'s path in config'.format(str(err)))
			sys.stderr.write('\nERROR: {}; check google auth token\'s path in config\n'.format(str(err)))
			sys.exit(301)
        # Tell Google we're using the admin directory API with our http object
        # then have it try and check if the email specified exists
		directory_service = build('admin', 'directory_v1', http=http) 
		request = directory_service.users().get(userKey = email)
		# Handle 'userKey not found' error, ie confirms a fake account
		self.logger.debug('Checking if "{}" exists in google apps directory'.format(email))
		try:
			response = request.execute()
			self.logger.warn('"{}" is a valid email address. Creating another user'.format(email))
			return True
		except HttpError:
			self.logger.info('"{}" is not a valid email address. Okay to use'.format(email))
			return False

        
    def create(self, email_domain='', auth_token=''):
		'''Makes a User object'''
		# Check the Email Domain for example.com
		self.logger.debug('Email domain attribute "{}" read from ChaffConfigure object'.format(email_domain))
		# If email_domain is blank replace with example.com 
		if email_domain == '' or None:
			self.logger.debug('Email domain, "{}", is blank or None, setting email domain to example.com'.format(email_domain))
			email_domain = '@example.com'
		else:
			email_domain = '@{}'.format(email_domain)
			self.logger.debug('Email domain "{}" will be used to chaff'.format(email_domain))
		# Make the name
		first_name, last_name = self._make_name()
		# Make the netid
		netid = self._make_netid(first_name, last_name, email_domain)
        # Make the email address
		email_address = self._make_email(netid, email_domain)
        # If email is valid, create a new netid & email
		while self._is_valid_google_account(email_address, auth_token):
			netid = self._make_netid(first_name, last_name, email_domain)
			email_address = self._make_email(netid, email_domain)
		# Fake email confirmed, continue with phony account details
		self.logger.debug('Creating a password...')
		password = self._jazz_password(self._rand_fields('password'))
		phone = self._rand_fields('phone')
		country = 'United States'
		ted = User(first_name, last_name, netid, email_address, password,
				phone, country)
		self.logger.info('Phone user "{} {}" created'.format(first_name, last_name))
		return ted

    




