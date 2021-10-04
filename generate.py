import json
import re
#http://moorearchive.org/viewer/nb07_03_11

f = open('glossary copy.json',)

data = json.load(f)
output = ''

def genSrc(type, src):
	#print("generating source")
	p = data[src][type]
	p_list = p.split(';')
	nb = []
	snippet = "<p>"+type + ": "
	print (p)
	for x in range (0, len(p_list)):
		print (len(p_list))
		if len(p_list[x]) > 7:
			nb = p_list[x].split()
			print (nb)
			#print(nb[1])
		if len(nb) >= 4:
			pages = ['']*(len(nb)-3)
			page = ''
			ext = ''
			for i in range(0, len(nb)-3):
				pages[i] = nb[len(nb)-1-i]
				#print (pages)
			#print (nb[1])
			src = nb[1].split('.')
			nblink = ['']*len(pages)
			#print (src)
			if len(src) == 3:
				for idx in range(0, len(pages)):
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
						page = str(int(pages[idx][:-1])).zfill(4)
						ext = page+"-verso"
					elif int(pages[idx])%2 == 1:
						page = str(int(pages[idx])).zfill(4)
						ext = page+"-recto"
					elif int(pages[idx])%2 == 0:
						page = str(int(pages[idx])).zfill(4)
						ext = page+"-verso"
					#print (ext)
					nblink[idx] = nblink[idx]+ext
			for i in range (0, len(nblink)):
				snippet = snippet + "<a href=\"" + nblink[i] + "\">nb" + src[0]+"-"+src[1]+"-"+src[2]+"-"+ext+"</a>"
				if i != len(nblink)-1:
					snippet = snippet + "; "
			if x != len(p_list)-1:
				snippet = snippet + "; "
		else:
			return ''
	snippet = snippet + "</p>"
	return snippet

		#print(snippet)

for x in range (0, 244):
	if data[x]["displayOnlyAnnotatedNamesDisplayGlossaryLinksTheRestAreForFutureReference"] == "Yes":
		birth = data[x]['birth']
		death = data[x]['death']
		if isinstance(data[x]['birth'], (int, long)):
			birth = str(birth)
		elif len(data[x]['birth']) == 1:
			birth = 'unknown'
		if isinstance(data[x]['death'], (int, long)):
			death = str(death)
		elif len(death) == 1:
			death = 'unknown'
		firstName = data[x]['first']
		print data[x]['lastOrFull']
		p1 = "<p><strong><font size=\"3\">" + data[x]['lastOrFull'] + ', ' + data[x]['first'] + "</font></strong><span style=\"font-size:x-small;\">" + ' (' + "</span><font size=\"-2.5\">" + birth + '-' + death + ')' +"</font></p>"
		if len(firstName) == 1:
			p1 = "<p><strong><font size=\"3\">" + data[x]['lastOrFull'] + "</font></strong><span style=\"font-size:x-small;\">" + ' (' + "</span><font size=\"-2.5\">" + birth + '-' + death + ')' +"</font></p>"
		p2 = "<p><font color=\"gray\" size=\"-1\">" + data[x]['generalDescription'] + "</font><br />"
		#print (p2)
		p3 = ''
		if 'descriptionOfRelationToMoore' in data[x]:
			p3 = "<p>" + data[x]['descriptionOfRelationToMoore'] + "</p>"

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


#print (output)

HTML_file = open("glossary.html", "w")
HTML_file.write(output.encode('utf8')+'\n')
HTML_file.close()

f.close()
