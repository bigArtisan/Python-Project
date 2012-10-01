"""
insert the well formated data into database

first create a table with reqiured fileds, country_name, date, ie ....
insert the data row by row, and omit the empty row. So the the column should be set NULL 
"""
import sys
import MySQLdb
from utils import *

try:
	conn = MySQLdb.connect("localhost",'root','','country_browserdb')
except MySQLdb.Error, e:
    print "Database Error %d: %s"%(e.args[0],e.args[1])
    sys.exit()

cursor = conn.cursor()

#create table country_browser
create_table = """CREATE TABLE country_browser 
	(Country VARCHAR(50),
    Date_time VARCHAR(10),
    bowser1 VARCHAR(10),
    bowser2 VARCHAR(10),
    bowser3 VARCHAR(10),
    bowser4 VARCHAR(10),
    bowser5 VARCHAR(10),
    bowser6 VARCHAR(10))"""
cursor.execute(create_table)


#call insert data
def insert_data(cursor, csvdata,country_name):

	#Insert country name
	bn = csvdata[0]
	insert_country = """INSERT INTO country_browser(Country,Date_time, bowser1, bowser2,bowser3,bowser4,bowser5,bowser6)
		VALUES("%s",'%s','%s','%s','%s','%s','%s','%s')"""%(country_name,bn[0],bn[1],bn[2],bn[3],bn[4],bn[5],bn[6])
	cursor.execute(insert_country)

	#insert data
	#empty csv file 
	
	for row in csvdata[1:]:
		insert_data = """INSERT INTO country_browser(Country,Date_time, bowser1, bowser2,bowser3,bowser4,bowser5,bowser6) 
			VALUES('',%s,%s,%s,%s,%s,%s,%s)"""%(row[0],row[1],row[2],row[3],row[4],row[5],row[6])

		cursor.execute(insert_data)

def main():
	jsonurl="http://api.worldbank.org/countries/?incomeLevel=LMC&format=json"
	country_isocode = retriveJson(jsonurl)
	country_url = generate_country_url(country_isocode)
	total_contry = len(country_url)
	count = 1
	invalid_country = []
	for k,v in country_url.items():
		country_name = k
		csvdata = download_csv(v)
		print "Inserting data ..."
		print 
		try:
			insert_data(cursor, csvdata, country_name)
			print "%s Insertion for country: %s successfull [%s remains]"%(count, country_name, total_contry-count)
			print
			count +=1
		except:
			print "Data of country %s is invalid"%(k)
			invalid_country.append(k)
			pass
	print "The follwing countries data are not avaiable:"
	for c in invalid_country:
		print c
	conn.commit()
		

if __name__=="__main__":
	main()



	


