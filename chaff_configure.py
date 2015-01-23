'''
Module to generate Config file and compile/prepare data.
Overwrites chaff_config if file exists.
'''

import ConfigParser
import argparse
import sys
import logging


# Set up logger
logger = logging.getLogger('Chaff.Configure')

class ChaffConfigure(object):
	'''Chaff Configure is a container class where the attributes of the
	ChaffConfigure object correlate to the ConfigParser values.'''
	# Instantiate by loading the config file and assigning attributes
	def __init__(self):
		self.logger = logging.getLogger('Chaff.Configure.ChaffConfigure')
		self.logger.debug('ChaffConfigure class instantiated')

				
	def new_config(self,configname):
		'''Makes a blank config file.'''
		with open(configname, 'w') as cfgfile:
			logger.debug('Writing out fields for config file {}'.format(configname))
			cfgfile.write('''# NOTE: This config file is for the Form's name='FOO', id='BAR' values in the HTML source.  
# Do NOT wrap the values in quotation marks
# If no value exists in your form, simply leave it blank\n\n''')
			Config = ConfigParser.ConfigParser()
			Config.add_section('URL Details')
			Config.set('URL Details', 'Form URL', '')
			Config.set('URL Details', 'Action URL', '')
			Config.set('URL Details', 'Method', '')
			Config.add_section('FormID')
			Config.set('FormID','First Name', '')
			Config.set('FormID','Last Name', '')
			Config.set('FormID','Full Name', '')
			Config.set('FormID','NetID', '')
			Config.set('FormID','Email', '')
			Config.set('FormID', 'Confirm Email', '')
			Config.set('FormID','Phone', '')
			Config.set('FormID','Country', '')
			Config.set('FormID','Password', '')
			Config.set('FormID','Confirm Password', '')
			Config.add_section('AuthInfo')
			Config.set('AuthInfo', 'JSON User Data $PATH/Filename', '')
			Config.set('AuthInfo','Email Domain', '')
			Config.set('AuthInfo','Google Auth Token $PATH/Filename', '')
			Config.write(cfgfile)
		logger.info('Config file "{}" created.'.format(configname))
		print 'Config file "{}" created.'.format(configname)


	def load_config(self,cfgfile):
		'''Opens a Chaff config file and attempts to set it's values as
		attributes to the ChaffConfigure object.'''
		self.logger.debug('Loading config file: {}'.format(cfgfile))
		config = ConfigParser.ConfigParser()
		# Check to see if filename specified exists
		try:
			with open(cfgfile) as cfg:
				pass
		except IOError:
				self.logger.error('Config file "{}" not found.'.format(cfgfile))
				sys.stderr.write('\nERROR: Config file "{}" not found.\n'.format(cfgfile))
				sys.exit(501)
		# Check to see if any sections or options are not present in file
		# Values can be blank
		try:
			config.read(cfgfile)
			self.conf_url = config.get('URL Details', 'Form URL')
			self.conf_action_url = config.get('URL Details', 'Action URL')
			self.conf_url_method = config.get('URL Details', 'Method')
			self.conf_full_name = config.get('FormID', 'full name')
			self.conf_first_name = config.get('FormID', 'first name')
			self.conf_last_name = config.get('FormID', 'last name')
			self.conf_netid = config.get('FormID', 'netid')
			self.conf_email = config.get('FormID', 'email')
			self.conf_confirm_email = config.get('FormID', 'confirm email')
			self.conf_password = config.get('FormID', 'password')
			self.conf_confirm_pword = config.get('FormID', 'confirm password')
			self.conf_phone = config.get('FormID', 'phone')
			self.conf_country = config.get('FormID', 'country')
			self.conf_json = config.get('AuthInfo', 'json User Data $PATH/Filename')
			self.conf_auth_email_domain = config.get('AuthInfo', 'Email Domain')
			self.conf_auth_token_file = config.get('AuthInfo',
										'Google Auth Token $PATH/Filename')
		except ConfigParser.NoSectionError as err: 
			self.logger.error('{}'.format(str(err)))
			sys.stderr.write('\nERROR: {}\n'.format(str(err)))
			sys.exit(502)
		except ConfigParser.NoOptionError as err:
			self.logger.error('{}'.format(str(err)))
			sys.stderr.write('\nERROR: {}\n'.format(str(err)))
			sys.exit(503)



def main():
	if args.new_config:
		conf_obj = ChaffConfigure()
		conf_obj.new_config(args.new_config)


# If user runs chaff_configure.py, it will print help unless using --new-config
if __name__ == '__main__':
	# Create args for new config file
	parser = argparse.ArgumentParser() 
	parser.add_argument('--new-config', nargs='?', const='chaff_config',
					help='Make a blank chaff_config file')
	args = parser.parse_args()
	# Display help if no options are chosen
	if len(sys.argv) == 1: 
		parser.print_help()
		sys.exit(0)
	main()
