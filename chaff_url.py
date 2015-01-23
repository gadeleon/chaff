'''
Handles all URL processing functions
'''

import urllib2
import logging

from bs4 import BeautifulSoup


# Set up logger
logger = logging.getLogger('Chaff.URL')

def find_method(url):
	'''Attempts to find the action URL and whether we POST or GET to in a
	dict. It's not 100% guaranteed to work (looking at you Javascript forms)'''
	site = urllib2.urlopen(url)
	logger.debug('Opening URL to search for method')
	soup = BeautifulSoup(site.read())
	logger.debug('Parsing URL for possible method')
	# We use find_all() to get tags/links in the 'form' tag
	for link in soup.find_all('form'):
		target_url = link.get('action')
		method = link.get('method')
		logger.debug('URL to act against {} found.'.format(link.get('action')))
		#target_url = link.get('action')
		logger.debug('Method {} found'.format(link.get('method')))
		#method = link.get('method')
		logger.info('Found method "{}"'.format(method))
		logger.info('Found action url "{}"'.format(target_url))
		return target_url, method
		

def find_fields(url):
	'''Creates a dict of labels and the associated IDs If it can't work,
		it suggests you get the info manually
	'''
	logger.debug('Finding fields for {}'.format(url))
	out = {}
	site = urllib2.urlopen(url)
	logger.debug('URL opened')
	soup = BeautifulSoup(site.read())
	logger.debug('URL parsed')
	for link in soup.find_all('form'): 
		# Try and parse a normal html form
		logger.info('Scanning code for possible fields...')
		for result in soup.find_all('label'):
			# Creates dict with {label : id} pair
			logger.debug('Pair found: {}, {}'.format(result.get_text(strip=True),
				result.get('for')))
			out[result.get_text(strip=True)] = result.get('for') 
	logger.debug('Parse complete')
	return out


def print_fields(label_dict):
	'''Prints out the values in find_fields()'s dict'''
	logger.debug('Printing key, item pair for url fields')
	logger.info('Possible Form Fields:\n\nLabel\tID')
	for key, value in label_dict.iteritems():
		print key + '\t' + value	
		
