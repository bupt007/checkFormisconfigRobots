#!/usr/bin/python
# coding:utf-8
# @author: pengfei filename: misconfigRobots.py


import requests
import urlparse
from optparse import OptionParser

'''
	This code is used to detect whether the site's robots.txt is misconfigured or not.
'''

def GetRobotsFile(url):
	'''
		Return a generator for the list of  the robots.txt's urls.
		@parameter1 url(str): The site which we will attack or inspect.
	'''
	# check response is 200
	url = url + '/robots.txt'
	resp = requests.get(url)	
	if resp.status_code == 200 :
		lines = resp.iter_lines()
		for line in lines:
			if line.startswith('Disallow:'):
				yield urlparse.urljoin(url,line[10:])

def checkFunc(url):
	'''
	Try post or get to do the request, use post because of there is maybe verb tampering vul.
	'''
	funcPool = [requests.get,requests.post]
	respPool = []
	for fun in funcPool:
		respPool.append(fun(url).status_code)
	if 200 in respPool:
		return True
	else:
		return False
def travseRobots(url):
	'''
	travse to test url list in robots.txt
	'''
	robotsURL = GetRobotsFile(url)
	for child_url in robotsURL:
		if checkFunc(child_url):
			print "There is vul in url: %s" % (child_url)

if __name__=="__main__":

	useage = "Do a check for website's robots.txt configuration"
	parser = OptionParser(useage=useage)
	parser.add_option('-u','--url',dest='url',help='the web url which you want to do the check. Note:the url should be the root directory, eg. http://www.baidu.com')

	(options,args) = parser.parse_args()

	if str(options.url).startswith("http:") or str(options.url).startswith("https:"):
		travseRobots(str(options.url))







