'''
Find a URLs fields and stuff them with fake datums!
'''

import logging
import argparse
import sys
from time import sleep

import requests

import chaff_account
import chaff_url
import chaff_configure


# Instantiate Logger object & override __name__ to 'Chaff' 
logger = logging.getLogger('Chaff')

# Default Console Handler for logger
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Default Formatter for handler
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
console.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console)


# Contianer class for arguments
class OptionArguments(object):
	def __init__(self):
		'''Container class for command line argumensts.'''
		self.logger = logging.getLogger('Chaff.OptionArguments')
		self.logger.debug('Insantiating OptionArgument class')
		# Create and parse arguments
		parser = argparse.ArgumentParser()	
		parser.add_argument('-v', '--version', action='version',
			version = '%(prog)s 0.7.0')	
		parser.add_argument('--entries', type=int, nargs='?', default=3,
			help='Int. Number of entries you wish to chaff (default: 3 entries)') 
		parser.add_argument('--delay', type=float, nargs='?', default=3.0,
			help='Float. Time interval between fake entries (default: 3.0 seconds)')
		parser.add_argument('--config', nargs='?', default='chaff_config',
			help='Specify a config file (default: chaff_config)')
		parser.add_argument('--parse-form', action='store_true',
			help='Parses the site to find the "for= <id>", method, and action URL to be added to the config file.')
		parser.add_argument('--debug', action='store_true',
			help='Display debug messages')
		# Display help if no values given
		#if len(sys.argv) == 1: 
		#	parser.print_help()
		#	sys.exit(0)
		args = parser.parse_args()
		self.args = args
		self.entries = self.args.entries
		self.delay = self.args.delay
		self.config = self.args.config
		self.parse_form = self.args.parse_form
		self.debug = self.args.debug
		

def align_data(user,configure):
	'''Creates a dict pairing ChaffConfigure and User attributes.'''
	logger.debug('Aligning config file with account data')
	return {configure.conf_full_name : user.full_name,
			configure.conf_first_name : user.first_name,
			configure.conf_last_name : user.last_name,
			configure.conf_netid : user.netid,
			configure.conf_email : user.email,
			configure.conf_confirm_email : user.email,
			configure.conf_password : user.password,
			configure.conf_confirm_pword : user.password,
			configure.conf_phone : user.phone,
			configure.conf_country : user.country}


def look_for_fields(url):
	'''Invokes chaff_url.find_fields() to find possible form fields.'''
	find_results = chaff_url.find_fields(url)
	chaff_url.print_fields(find_results)
	target, method = chaff_url.find_method(url)
	# Rudimentary checking for URL results
	if len(find_results) == 0:
		logger.warn('Unable to find the fields from {}. Try getting them manually from the web page.'.format(url))
	if target == None:
		logger.warn('Unable to find action_url from {}. Try getting manually from the web page.'.format(url))
	if method == None:
		logger.warn('Unable to find method from {}. Try getting manually from the web page.'.format(url))
	sys.exit(0)
	
# Compile and then POST or GET the fake data
def chaff(url, user, configure, method, action_url):
	'''Align User object data to Configure object data and stuff into a url

	Arguments:
		url -- The url you would like to chaff
		user -- The User object which contains fake user information
		configure -- The Configure object which contains the form/labels of url
		method -- Generally POST or GET
		action_url -- The URL where chaff POSTS or GETS its data 

	'''	
	payload = align_data(user,configure)
	if method.upper() == 'POST':  
		requests.post(action_url, payload)
	elif method.upper() == 'GET':
		requests.get(url + action_url, params=payload)
	logger.debug('Phony user {} stuffed into url {} as a {} to {}'.format(user.full_name,
			url, method, action_url))
	logger.info('Stuffing phony account details: {!s}'.format(user))


# Parse config file and confirm we want to chaff, then GET or POST
# the info based on the form's requirements (provided the account is fake)
def main():
	options = OptionArguments()
	if options.debug:
		logger.setLevel(logging.DEBUG)
		console.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)
	configure = chaff_configure.ChaffConfigure()
	configure.load_config(options.config)
	form = configure.conf_url
	if options.parse_form:
		look_for_fields(form)
	prompt = raw_input('\n\nWARNING: About to send chaff based on info from config file "{}"; type "Y" to continue: '.format(options.config))
	if prompt not in ['y', 'Y', 'yes', 'YES', 'Yes']:
		logger.info('Received input "{}." Exiting...'.format(prompt))
		sys.exit(0)
	generator = chaff_account.UserGenerator(configure.conf_json)
	auth = configure.conf_auth_token_file
	email_domain = configure.conf_auth_email_domain
	action_url = configure.conf_action_url
	method = configure.conf_url_method
	# Make account(s) and chaff it!
	for _ in range(options.entries):		
		account = generator.create(email_domain, auth)
		chaff(form, account, configure, method, action_url)
		sleep(options.delay)
			
						
if __name__ == '__main__':
	main()
