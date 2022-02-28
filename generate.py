import json
import re
import time
import datetime
#import virtualtime
from datetime import datetime, date, time
#http://moorearchive.org/viewer/nb07_03_11

f = open('glossary.json',)
#virtualtime.enable()
data = json.load(f)
output = ''

# function to convert string to time
def convertTime(time_string):
	date_var = time.strptime(time_string, '%m/%d/%Y')
	return date_var

# the function used to generate the notebook source, for stuff like quote/see/cited
def genSrc(type, id):
	p = data[id][type]
	p_list = p.split(';') # ";" is used to separate two notebook sources in the spreadsheet

	nb = [] #NB string list for notebook references
	snippet = "<p class=\"relevance_"+type+"\">" +type.capitalize() + ": "
	if type == "quotationAbout":
		snippet = "<p class=\"relevance_"+type+"\">" +"Quotation About" + ": "
	#print (p_list) #print the source to console
	for x in range (0, len(p_list)):
		#print (len(p_list)) #word count of the message if necessary
		if len(p_list[x]) == 1 and len(p_list[x]) == 3: #'-' or '---'
			print("the entry is empty")
		elif len(p_list[x]) > 16: #16 is the minimum length of a valid message
			#print(p_list[x])
			nb = p_list[x].split()
			#print (nb) #print the notebook if necessary
		elif len(p_list[x])	< 16:
			print("the message" + p_list[x] + "might be invalid")
		if len(nb) >= 4: # the NB list is structured as ['Notebook', '07.04.01', 'pages', '101r', '103r'], so the minimum length is 4
			pages = ['']*(len(nb)-3) #create a list of pages based on length
			page = ''
			ext = ''
			for i in range(0, len(nb)-3):
				pages[i] = nb[len(nb)-1-i]
			#print (pages)
			src = nb[1].split('.') #split the notebook number (07.04.01) into a list of [07, 04, 01]
			#print (src)
			nblink = ['']*len(pages) #notebook links to generate
			if len(src) == 3:
				for idx in range(0, len(pages)):
					idx = len(pages)-idx-1
					if pages[idx][-1] == ',' or pages[idx][-1]=='.':
						pages[idx] = pages[idx][:-1]
					nblink[idx] = 'http://moorearchive.org/custom/notebooks/#doc='+src[0]+'-'+src[1]+'-'+src[2]+'&page=nb'+src[0]+'_'+src[1]+'_'+src[2]+'_'
					if '-' in pages[idx]:
						startPage = pages[idx].split('-')[0]
						if startPage[-1] == 'r':
							page = str(int(startPage[:-1])).zfill(4)
							ext = page+"-recto"
						elif startPage[-1] == 'v':
							page = str(int(startPage[:-1])).zfill(4)
							ext = page+"-verso"
						elif int(startPage)%2 == 1:
							page = str(int(startPage)).zfill(4)
							ext = page+"-recto"
						elif int(startPage)%2 == 0:
							page = str(int(startPage)).zfill(4)
							ext = page+"-verso"
					elif pages[idx][-1] == 'r':
						#print (str(int(pages[idx][:-1])).zfill(4))
						page = str(int(pages[idx][:-1])).zfill(4)
						ext = page+"-recto"
					elif pages[idx][-1] == 'v':
						if len(pages[0]) != 1:
							page = str(int(pages[idx][:-1])).zfill(4)
							ext = page+"-verso"
						else:
							print ("please check entry No."+str(id)+" formatting");
					elif pages[idx].isdigit():
						if int(pages[idx])%2 == 1:
							try:
								page = str(int(pages[idx])).zfill(4)
								ext = page+"-recto"
							except:
								print("please check entry No."+str(id)+" formatting")
						elif int(pages[idx])%2 == 0:
							try:
								page = str(int(pages[idx])).zfill(4)
								ext = page+"-verso"
							except:
								print("please check entry No."+str(id)+" formatting")
						#print (ext)

					elif pages[idx].isdigit() == False:
						print ("please check entry No."+str(id)+" formatting")
					nblink[idx] = nblink[idx]+ext

					if idx==len(pages)-1:
						snippet = snippet + "Notebook " + src[0]+"."+src[1]+"."+src[2]+" page " +"<a class=\"glossary_reference\" href=\"" + nblink[idx] + "\">"+ext+"</a>"
					else:
						snippet = snippet + "<a class=\"glossary_reference\" href=\"" + nblink[idx] + "\">"+ext+"</a>"
					if idx != 0:
						snippet = snippet + ", "

			'''for i in range (0, len(nblink)):
				if i==0:
					snippet = snippet + "Notebook " + src[0]+"."+src[1]+"."+src[2]+" page " +"<a class=\"glossary_reference\" href=\"" + nblink[i] + "\">"+ext+"</a>"
				else:
					snippet = snippet + "<a class=\"glossary_reference\" href=\"" + nblink[i] + "\">"+ext+"</a>"
				if i != len(nblink)-1:
					snippet = snippet + ", "'''
			if x != len(p_list)-1:
				snippet = snippet + "; "
		elif len(nb) < 3:
			print ("page info is missing for entry " + data[id]["lastOrFull"])
	snippet = snippet + "</p>"
	return snippet

	#print(snippet)

for x in range (0, len(data)):
	if data[x]["displayOnlyAnnotatedNamesDisplayGlossaryLinksTheRestAreForFutureReference"] == "Yes":
		birth = data[x]['birth']
		death = data[x]['death']
		if isinstance(data[x]['birth'], (int, int)): #used to be (int, long) for python 2
			birth = str(birth)
		elif len(data[x]['birth']) == 1:
			birth = 'unknown'
		if isinstance(data[x]['death'], (int, int)):
			death = str(death)
		elif len(death) == 1:
			death = 'unknown'
		firstName = data[x]['first']
		#print (data[x]['lastOrFull']) #print the name for debug
		try:
			birth = datetime.strptime(birth,'%m/%d/%Y').strftime("%B %-d, %Y")
		except:
			if len(birth)<=4:
				birth = birth #do nothing
				#birth = 'c. '+birth
			elif birth == "unknown":
				birth = "?"
			elif birth[-1]=='E' and birth[0]!='c':
				birth = birth #do nothing
				#birth = 'c. ' + birth
			elif birth[-1] == 'Z':
				birth = birth.split('T')[0]
				birth = datetime.strptime(birth,'%Y-%m-%d').strftime("%B %-d, %Y")
				#print ("datetime needs reformatting")
		try:
			death = datetime.strptime(death,'%m/%d/%Y').strftime("%B %-d, %Y")
		except:
			if len(death)<=4:
				death = 'c. '+death
			elif death == "unknown":
				death = "?"
			elif death[-1]=='E' and death[0]!='c':
				death = 'c. ' + death
			elif death[-1] == 'Z':
				death = death.split('T')[0]
				death = datetime.strptime(death,'%Y-%m-%d').strftime("%B %-d, %Y")
			#print(datetime.strptime(birth,'%m/%d/%Y').strftime("%B %d, %Y")) #display the date in correct format
		db_exp = "" #death & birth expression
		if death=="?" and birth=="?":
			db_exp = " - "
		elif death=="?":
			db_exp = "b. " + birth
		elif birth=="?":
			db_exp = "d. " + death
		else:
			db_exp = birth + ' - ' + death
		p1 = "<p><strong class=\"person_name\">" + data[x]['lastOrFull'] + ', ' + data[x]['first'] + "</strong><span class=\"birth_death\" >" + ' (' + "</span>" + db_exp + ')' +"</p>"
		if len(firstName) == 1:
			p1 = "<p><strong class=\"person_name\">" + data[x]['lastOrFull'] + "</strong><span>" + ' (' + "</span class=\"birth_death\" >" + db_exp + ')' +"</p>"
		p2 = "<p class=\"generalDescription\">" + data[x]['generalDescription'] + "<br />"
		#print (p1)
		p3 = ''
		if 'descriptionOfRelationToMoore' in data[x]:
			p3 = "<p class=\"relationToMoore\">" + data[x]['descriptionOfRelationToMoore'] + "</p>"

		p4 = ''
		output = output + p1+p2+p3
		nb = []
		nblink = ''
		if 'see' in data[x]:
			if len(data[x]['see']) > 3:
				r = genSrc('see', x)
				if r != '':
					output = output + r
		if 'cited' in data[x]:
			#if data[x]['cited'] != '-' and data[x]['cited'] != '---':
			if len(data[x]['cited']) > 3:
				r = genSrc('cited', x)
				if r != '':
					output = output + r
		if 'quoted' in data[x]:
			if len(data[x]['quoted']) > 3:
				r = genSrc('quoted', x)
				if r != '':
					output = output + r
		if 'quotationAbout' in data[x]:
			if len(data[x]['quotationAbout']) > 3:
				r = genSrc('quotationAbout', x)
				if r != '':
					output = output + r
		output = output+'<br />'
'''
				p3 = re.sub(nb[1], '', p3, 1)
				htmltag = "<a href=\"" + nblink[0] +"\">"+"Notebook " +nb[1]+"</a>"
				p3 = re.sub('Notebook ', htmltag, p3, 1)
'''
output = "<link rel=\"stylesheet\" type=\"text/css\" href=\"styles.css\" /><meta charset=\"utf-8\">" + output

#print (output)

HTML_file = open("glossary.html", "w")
#HTML_file.write(output.encode('utf8')+'\n') #python 2 version
#HTML_file.write((str(output.encode('utf-8').decode('utf-8'))+'\n')[2:])
#HTML_file.write((str(output.encode('utf-8'))+'\n'))
HTML_file.write(output)
HTML_file.close()

f.close()
