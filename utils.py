
"""
The utils includes four functions that utilized in the main programme.
1. retriveJson
	Download json data according to the word bank api, and retrieve the isocode of the each country.
2. generate_country_url
	Substitute the iso_code of the csv_url.
3. download_csv
	Download csv file from the url
4. insert_data
	Insert the csv file into the database

"""
import urllib2
import csv
from pprint import pprint as pprint
import urllib2
import simplejson
import string

def generate_country_url(country_isocode):
	""" generate a dict with country name as the key and the url as value"""
	country_url = {}
	iso_url="http://gs.statcounter.com/chart.php?statType_hidden=browser&region_hidden=AL&granularity=yearly&statType=Browser&fromYear=2008&toYear=2012&csv=1"
	for k,v in country_isocode.items():
		country_name = k
		url = "http://gs.statcounter.com/chart.php?statType_hidden=browser&region_hidden=%s&granularity=yearly&statType=Browser&fromYear=2008&toYear=2012&csv=1"%(v)
		country_url[country_name] = url
	return country_url

#input url as the argument and return csvdata, which is a list of list
def download_csv(url):
	"""retrive the csv data from the url"""
	data = urllib2.urlopen(url)
	csvData = list(csv.reader(data))
	return csvData


def retriveJson(jsonurl):
	"""download the json data and retrieve the country isocode dict"""

    data = urllib2.urlopen(jsonurl)

    jdata = simplejson.load(data)
    
    #create an empty dict to store the country name and isocode
    country_isocode = {}

    #the country data begins at the 2nd element
    table = string.maketrans("","")
    for elem in jdata[1:]:
        for item in elem:
        	#decorate the country name for mysql reading, no whitesapce and - 
			country_name = "_".join(item['name'].translate(table, string.punctuation).split())
			country_isocode[country_name] = item['iso2Code']
	
	return country_isocode



def insert_data(cursor,csvdata,country_name):
	""" Insert the data into the table country_browser"""
	#Insert country name
	insert_country = """INSERT INTO country_browser(Country,Date_time, IE,Chrome,Firefox,Safari,Opera,Other)
		VALUES("%s",'-','-','-','-','-','-','-')"""%(country_name)
	cursor.execute(insert_country)

	#insert data
	#empty csv file 
	if  len(csvdata[1:]) < 1:
		pass
	else:

		for row in csvdata[1:]:
			print len(csvdata[1:])
			insert_data = """INSERT INTO country_browser(Country,Date_time, IE,Chrome,Firefox,Safari,Opera,Other)\
	    	VALUES('',%s,%s,%s,%s,%s,%s,%s)"""%(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
    		cursor.execute(insert_data)







