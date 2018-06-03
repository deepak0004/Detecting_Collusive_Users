import ConfigParser
import sys

"""
	This module is for making the setting of API
	keys in a serializable manner. The api key
	file is passed as the first command line
	argument and the history file which stores
	the number of the last API key used as the
	command line argument.

"""


def populate_Settings(sfile, hfile):

	settings_file = sfile
	history_file = hfile

	#print settings_file
	# Read the history file
	with open(history_file) as f:
		content = f.readlines()

	last = 0

	#print(content)

	last = int(content[0])

	config = ConfigParser.ConfigParser()
	config.readfp(open(settings_file))

	minVal = 57
	'''
	while minVal:
		try:
			print config.get('API Keys ' + str(minVal), 'API_KEY')
			minVal += 1
		except ConfigParser.NoSectionError:
			break
    '''
	minVal = minVal - 1
	

	if last == minVal:
		current = 1
	else:
		current = last + 1


	fw = open("apikeys/api_history.txt", "w")

	fw.write(str(current))

	fw.close()

	# Read config settings
	

	# Random API key selection 
	consumer_key= config.get('API Keys ' + str(current), 'API_KEY')
	consumer_secret = config.get('API Keys ' + str(current), 'API_SECRET')
	access_token = config.get('API Keys ' + str(current), 'ACCESS_TOKEN')
	access_token_secret = config.get('API Keys ' + str(current), 'ACCESS_TOKEN_SECRET')

	return consumer_key, consumer_secret, access_token, access_token_secret

if __name__ == '__main__':
	populate_Settings()
