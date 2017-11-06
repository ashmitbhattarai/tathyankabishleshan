#! usr/local/lib python2.7
# -*- coding: utf-8 -*-
from collections import defaultdict
from pyspark import SparkContext
from functools import partial
import timeit,json,io
import os,sys,string,re,csv
sys.path.append("/home/ashmit/Legion/myproject/newproject/scripts/tathyanka")

reload(sys)
sys.setdefaultencoding('utf8')

from nepnb.nepnb import classify

nepanalyze = classify()
months = {u'असोज':"6",
		u'कार्तिक':"7",
		u'असार':"3",
		u'आश्विन':"6",
		u'जेष्ठ':"2",
		u'भाद्र':"5",
		u'वैशाख':"1",
		u'मंसिर':"8",
		u'पुस':"9",
		u'माघ':"10",
		u'फाल्गुन':"11",
		u'चैत्र':"12",
		u'श्रावण':"4"}

names = open("/home/ashmit/Legion/myproject/newproject/scripts/tathyanka/files/names.txt","r+")
fullname= names.read().decode("utf-8","strict").split("\n")
lname = sorted(set(list([x.split(" ")[-1].strip() for x in fullname])))
fname = sorted(set(list([x.split(" ")[0].strip() for x in fullname])))
names.close()
def select_text(tupledata):
	name = tupledata[0]
	text = tupledata[1]
	sents = []
	filedict = defaultdict(list)
	filelist = []
	newdict = {}
	for each in text[1]:
		if name.split(" ")[-1] in each and len(each.split(" "))>5:
			sents.append(text[1].index(each)+8)
	filedict[name] = {text[0].replace("file:",""):sents}
	return (filedict)

def reducer(val1,val2):
	semifinaldict={}
	for name in val2:
		if name in val1.keys():
			semifinaldict[name]=dict(val2[name].items()+val1[name].items())
		else:
			semifinaldict[name] = val2[name]
	finaldict=dict(val1.items()+semifinaldict.items())
	return (finaldict)
def categorically(tupledata,category):
	if category != "names":
		forbidden = [each for each in fullname if tupledata[0] in each]
		for each in forbidden:
			if each in "\n".join(tupledata[1][1]):
				return;
	return tupledata
def createrecord(category):
	sc = SparkContext(appName="tathyanka")
	inputFile = r"file:///home/ashmit/Legion/myproject/newproject/module/२०७१/*/*/*"
	data = sc.wholeTextFiles(inputFile).coalesce(8).cache()
	path = "/home/ashmit/Legion/myproject/newproject/scripts/tathyanka/files"
	namefile = open(os.path.join(path,category+".txt"),"r+")
	namelist=unicode(namefile.read()).split("\n")
	withname = data.map(lambda x : (x[0],x[1].split("\n")[6:]))
	namelist = sc.parallelize(namelist).coalesce(3)
	newlist = namelist.cartesian(withname)\
				.filter(lambda x: x[0] in "\n".join(x[1][1]))\
				.filter(partial(categorically,category=category))\
				.map(select_text).reduce(reducer)
	with io.open(category+".txt","w",encoding="utf-8") as f:
		f.write(unicode(json.dumps(newlist, ensure_ascii=False)))
	sc.stop()
	return 0

def extract_sents(tupledata,filenamedict):
	textlist = tupledata[1]
	sentences= []
	filelist = filenamedict[tupledata[0]]
	for each in filelist:
		sentences.append(textlist[int(each)-2])
	return(sentences)

def findrecord(category,name):
	json_file=open("/home/ashmit/Legion/myproject/newproject/scripts/tathyanka/tb/final/"+category+".txt","r+")
	content=json.load(json_file)
	json_file.close()
	info = content[name]
	filenamelist = info.keys()
	monthcount = defaultdict(int)
	for each in filenamelist:
		month = each.split("/")[8]
		if month in months.keys():
			monthcount[months[month]] += len(info[each])
	del content
	scorelist = defaultdict(list)
	sc1 = SparkContext(appName="tathyanka")
	data=sc1.wholeTextFiles(",".join(filenamelist)).coalesce(3)
	sentences = data.map(lambda x:(x[0].replace("file:",""),x[1].split("\n")))\
					.flatMap(partial(extract_sents,filenamedict=info))
					# .flatMap(lambda x: x[1][int(each)-1] for key,values in filenamedict.items() for each in values)
	sentlist=sentences.collect()
	sc1.stop()
	del info,filenamelist,data,sentences
	for each in sentlist:
		score= nepanalyze.execute(each)
		if score <= 0.25:
			scorelist["negative"] += [each]
		elif score >= 0.75:
			scorelist["positive"] += [each]
		else:
			scorelist["neutral"] += [each]
	datalist = {}
	datalist["namez"] = name
	datalist["score"] = scorelist
	datalist["month"] = monthcount
	datalist["pos"] = len(scorelist["positive"])
	datalist["neg"] = len(scorelist["negative"])
	datalist["neu"] = len(scorelist["neutral"])
	del sentlist,scorelist,monthcount
	return datalist
# start1 = timeit.default_timer()
# createrecord("names")
# print timeit.default_timer() - start1
# findrecord("names",unicode("सुशील कोइराला"))