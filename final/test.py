#!-*- coding: utf-8 -*-
import os,sys,string,re,csv
from collections import defaultdict
# from pyspark import SparkContext
from functools import partial
import timeit,json,io
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/ashmit/Legion/myproject/newproject/scripts/tathyanka")
from nepnb.words import *
# start1 = timeit.default_timer()

# """sc = SparkContext(appName="tathyanka")
# inputFile = "file:/home/ashmit/Legion/myproject/newproject/module/२०७१/कार्तिक/१९/भ्रष्टाचार गरे मन्त्रीलाई पनि एक मिनेटमै निकाल्छुः प्रधानमन्त्री.txt,file:/home/ashmit/Legion/myproject/newproject/module/२०७१/कार्तिक/३/कांग्रेसमामहासमितिबोलाउनसुजाताकोहस्ताक्षरअभियान।.txt"
# data = sc.wholeTextFiles(inputFile).coalesce(4).cache()
# print data.first()
# sc.stop
# print timeit.default_timer() - start1"""
# path = "/home/ashmit/Legion/myproject/newproject/module/२०७१/"
# for root,dirs,files in os.walk(path):
# 	for each in files:
# 		if "," in each:
# 			print each
# 		# try:
# 			# print os.chdir(root+"/"+each)
# 		# except IOError:
# 			# pass
# # from collections import defaultdict

# # a=[("13.5",[100])]
# # b=[("13.5",[100]), ("15.5", [100])]
# # c=[("15.5",[100]), ("16.5", [100])]
# # input=[a,b,c]

# # output=defaultdict(list)
# # for d in input:
# #         for item in d:
# #            output[item[0]]+=item[1]
# # print dict(output)
# val1={"mz":{"/home/ashmit/Legion/myproject/newproject/module/२०७१/असार/२६/यस्ता छन् नेपाल र ओली समूहका उम्मेदवार.txt": [268, 279, 303, 318]},
# 		"me":{"/home/ashmit/Legion/myproject/newproject/module/२०७१/असोज/३०/संवादसमितिमाभट्टराईकोरुलिङ-भोलिसम्ममासहमतिकोप्रस्ताव।.txt": [10]}}
# val2 = {"me":{"/home/ashmit/Legion/myproject/newproject/module/२०७१/श्रावण/१३/मोदी भ्रमणको बेला ऊर्जा विकास सम्झौता गर्न दलहरु सहमत.txt": [24, 27],\
# 		},"ml":{"/home/ashmit/Legion/myproject/newproject/module/2071/श्रावण/१३/मोदी भ्रमणको बेला ऊर्जा विकास सम्झौता गर्न दलहरु सहमत.txt": [24, 27]}}
# def merge_two_dicts(x, y):
# 	z = x.copy()
# 	z.update(y)
# 	return z
# def reducer(val1,val2):
# 	finaldict={}
# 	semifinaldict={}
# 	for name in val2:
# 		if name in val1.keys():
# 			semifinaldict[name]=dict(val2[name].items()+val1[name].items())
# 		else:
# 			semifinaldict[name] = val2[name]
# 	finaldict=dict(val1.items()+semifinaldict.items())
# 	return (finaldict)
# print reducer(val1,val2)
# names = open("/home/ashmit/Legion/myproject/newproject/scripts/tathyanka/files/names.txt","r+")
# fullname= names.read().decode("utf-8","strict").split("\n")
# lname = sorted(set(list([x.split(" ")[-1].strip() for x in fullname])))
# fname = sorted(set(list([x.split(" ")[0].strip() for x in fullname])))
# namelist =[]
# for each in lname:
# 	for every in fname:
# 		if " ".join([every,each]) not in fullname:
# 			namelist.append(" ".join([every,each]))
# for thats in namelist:
# 	names.write(thats+"\n")
# names.close()
text = """'आफैंले भोगेको देखेको र अनुभव गरेको कुरा नै पुस्तकमा आएको हो ।
पुस्तकमा मैले आफनो प्रंशसा हैन आफनै कथा पस्केको हुँ,'  नेपाली सेनाका पूर्व प्रधानसेनापति रुकमाङ्गद कटवालले जंगी स्वभावमा शनिवार साक्षात्कार तथा  पुस्तक हस्ताक्षर कार्यक्रममा भने, 'पुस्तक नेपाल आमा तथा नेपाली सेनाको नूर गिराउने विरुद्धमा कदापी  छैन ।'
आफू सेनाको जर्नेलको जिम्मेवारीमा हुँदा आम नेपाली जनताले समेत थाहा पाएका कुरा नै पुस्तकमा लेखिएको उनले दाबी गरे ।  अतिरञ्जित तवरले  र  कोरा कल्पना  पुस्तकमा नलेखिएको उनले प्रष्टाए ।
एमाओवादी अध्यक्ष पुष्पकमल दाहालले उनको पुस्तकलाई बाहियात भएको टिप्पणी गरिरहेको बेला कटवालले आफ्नो कथा सबैलाई राम्रै लाग्छ भन्ने पनि नरहेको बताए  ।  'अव मैले कालो ठानेको मान्छेलाई आफ्नै श्रीमतीले कृष्ण ठान्छिन् भने म के गरुँ,' उनको तर्क थियो ।
र्‍याडम रिर्डस अफ सोसाइटीले गरेको साक्षात्कार कार्यक्रममा पोखरा आइपुगेका कटवाल समक्ष पाठकले पुस्तकमा अतिररिञ्जत कुराहरु बढी आएको भन्दै प्रश्नहरुको चाङ तेर्साएका थिए ।
कडा शैलीमा प्रस्तुत भएका  कटवालले चितबुझ्दो जवाफ भने धेरैको दिन सकेनन् ।  सबै कुरा पुस्तकमै छ भन्दै  सोधिएका प्रश्नहरुको ठाडो रुपमा उत्तर बंगाएर अन्यत्र मोडी दिन्थे ।  निकै ठुलो भीड उनलाई सुन्न सभाहलमा उठेर पनि घण्टौं सम्म  सुन्न आतुर देखिएका थिए ।  दौरासुरुवाल र ढाका टोपीमा सजिएर आएका उनले आफु प्रधानसेनापति हुँदा एउटा संस्थाको पक्षमा नभई जनताको पक्षामा रहेर निर्णय लिएको बताए ।
प्रधानसेनापतिबाट  अवकाश पत्र थमाएको बेला कुनै अप्रिय निर्णय गर्न लाग्नु भएको थियो भन्ने पाठकका जिज्ञासामा उनले  त्यतिबेला सबैको चाहना बुझेर नै  आफूले निर्णय   गर्न सक्ने  प्रतिउत्तर दिए ।
उनले एउटाको निर्णयले मात्रै केही नहुने  बताए ।  म्याद नथपेको भए के हुन्थ्यो भन्ने जिज्ञासामा कटुवालले  'अन द स्पट' गर्ने कुरा हो  त्यतिबेला सबै सहयोगीको सल्लाहले नै अघि बढिन्थ्यो' भन्दै आफनो धारणा राखे ।
उनले पुस्तक लेख्दा  राष्ट्रको  गोपनियता कही भंग नभएको  र कसैले भन्छ भनेर कहाँ निर भएको छ देखाउन समेत चुनौती दिए ।
उनले गिरिजाप्रसाद कोइरालाले बेबी किङ राख्ने बारेमा आफु सँग सल्लाह गरेको बताए ।  उनले आफूलाई राजावादीको आरोपको समेत खण्डन गरे । नेताहरुले  ०६२/०६३ मा  राजसँग दाम चढाएकै हुन् यो आम नेपालीलाई थाहा छ', उनले भने, 'मलाई राजावादी भन्नेहरुले त्यो बेला राजा मानेकै हुन् ।' उनले पूर्व प्रधानमन्त्री बाबुराम भट्टराईले समेत 'सेरोमेनियल किङ' को पक्षमा रहेको दाबी गरे ।
झण्डै डेढ घण्टाको कार्यक्रममा पत्रकार महासंघ कास्कीका अध्यक्ष रामकृष्ण ज्ञवालीले सहजकर्ताको भुमिका निर्वाह गरेका थिए भने पुस्तकका सहलेखक किरण भण्डारी  तथा सम्पादक सुदीप श्रेष्ठले पनि उठेका केही जिज्ञासाका जवाफ दिएका थिए ।
कार्यक्रम समापनपछि उनीसँ  पुस्तक हस्ताक्षर गर्नेहरुको पनि भीड बढेको थियो ।
प्रकाशित मिति: २०७१ भाद्र १४ ०९:०६"""
subsentlist=[]
sentlist = []
for each in text.replace("\n","").replace("'",'').split("।"):
	subsentlist=[]
	for every in each.split():
		if every:
			every = stemword(every)
		if every:
			every = clean_words(every)
		if every:
			subsentlist.append(every)
	sentlist.append(" ".join(subsentlist))

for each in sentlist:
	print each
