# -*- coding: utf8 -*-
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from time import sleep, strftime
from datetime import datetime
import json
import time
import sys

#https://www.skyscanner.com.tw/transport/flights-from/tpet/180419?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home
#https://www.skyscanner.com.tw/transport/flights-from/tpet/180419/180426?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home
#https://www.skyscanner.com.tw/transport/flights-from/tpet/180419/180426?adults=3&children=0&adultsv2=2&childrenv2=15&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home
#https://www.skyscanner.com.tw/transport/flights-from/tpet/180419/180426?adults=5&children=1&adultsv2=4&childrenv2=15%7c3&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home
#https://www.skyscanner.com.tw/transport/flights-from/tpet/180419/180426?adults=7&children=2&adultsv2=6&childrenv2=15%7c3%7c10&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home
#https://www.skyscanner.com.tw/transport/flights-from/tpet/180419/180426?adults=9&children=0&adultsv2=6&childrenv2=15%7c14%7c13&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home
#https://www.skyscanner.com.tw/transport/flights-from/tpet/180419/180426?adults=7&children=2&adultsv2=6&childrenv2=12%7c11%7c10&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home
#https://www.skyscanner.com.tw/transport/flights-from/tpet/180419/180426?adults=6&children=1&adultsv2=6&childrenv2=0%7c1%7c2&infants=2&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home
#https://www.skyscanner.com.tw/transport/flights-from/tpet/180419?adults=6&children=1&adultsv2=3&childrenv2=15%7c14%7c13%7c0%7c1%7c2&infants=2&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home
ListAge = []

def StartDate(Date):
	Bounday = datetime.strptime(Date, "%Y-%m-%d")
	Today = datetime.now()     
	dayCount = (Bounday - Today).days            
	if (dayCount < -1):
		return False
	elif (dayCount >= -1):
		return True
		
def EndDate(StartDate, EndDate):
	Bounday = datetime.strptime(StartDate, "%Y-%m-%d")
	Today = datetime.now()  
	dayCount = (Bounday - Today).days        
	if (dayCount < -1):
		return False
	elif (dayCount >= -1):         
		ReturnDay = datetime.strptime(EndDate, "%Y-%m-%d")
		dayCount2 = (ReturnDay - Bounday).days
		if (dayCount2 >= 1):
			return True
		else:
			return False
       	
   
def splitDate(Date):
	Date = str(Date)	
	Year = Date[2:4]
	Month = Date[5:7]
	Day = Date[8:10]
	GoBackDay = Year + Month + Day	
	return GoBackDay

	
def Booting():
	global ListAge
	TripType = input(">>>請輸入訂票種類來回(RT)、單程(OW):")
	if (TripType == "OW"):
		GoDate = input(">>>請輸入要去的日期xxxx-xx-xx:")		
		if (StartDate(GoDate) is True):			
			Adults = input(">>>請輸入大人數:")
			AdultsNumber = int(Adults)
			Children = input(">>>請輸入小孩數:")
			ChildrenNumber = int(Children)
			if(ChildrenNumber / AdultsNumber == 0):
				while(ChildrenNumber != 0):
					age = input(">>>請輸入每一個小孩的年齡:(0~15)")
					if (age >= 0 and age <= 15):
						ListAge.append(age)
						ChildrenNumber -= 1
					else:
						print("超過小孩年齡(0~15)\n")
				Destination = input("請輸入想去的地方:(注:需要知道想去的地方在skyscanner得簡寫名稱)")
				SetWebUrl(TripType, GoDate, 0, Destination, Adults, Children, ListAge)
			else:
				print("每一位大人只能帶兩位小朋友\n")
				Booting()		
		else:
			print("日期錯誤\n")
			Booting()			
	elif(TripType == "RT"):
		GoDate = input(">>>請輸入要去的日期xxxx-xx-xx:")
		BackDate = input(">>>請輸入回程的日期xxxx-xx-xx:")
		if (StartDate(GoDate) is True and EndDate(GoDate, BackDate) is True):
			Adults = input(">>>請輸入大人數:")
			AdultsNumber = int(Adults)
			Children = input(">>>請輸入小孩數:")
			ChildrenNumber = int(Children)
			if(ChildrenNumber / AdultsNumber == 0):
				while(ChildrenNumber != 0):
					age = input(">>>請輸入每一個小孩的年齡:(0~15)")
					if (age >= 0 and age <= 15):
						ListAge.append(int(age))
						ChildrenNumber -= 1
					else:
						print("超過小孩年齡(0~15)\n")					
				Destination = input("請輸入想去的地方:(注:需要知道想去的地方在skyscanner得簡寫名稱)")
				SetWebUrl(TripType, GoDate, BackDate, Destination, Adults, Children, ListAge)
			else:
				print("每一位大人只能帶兩位小朋友\n")
				Booting()
		else:
			print("日期錯誤\n")
			Booting()			

def SetWebUrl(TripType, GoDate, BackDate, Destination, Adults, Children, ListAge):	
	adultsNumber = 0
	childrenNumber = 0
	infantsNumber = 0
	message = ""
	
	if (GoDate != None and BackDate != 0):
		GoDate = splitDate(GoDate)
		BackDate = splitDate(BackDate)
	elif (GoDate != None):
		GoDate = splitDate(GoDate)
	
	for i in range(len(ListAge)):
		if (ListAge[i] >= 0 and ListAge[i] <= 1):
			infantsNumber += 1
		elif(ListAge[i] >= 13 and ListAge[i] <= 15):
			adultsNumber += 1
		else:
			childrenNumber += 1
			
	Index = "https://www.skyscanner.com.tw/transport/flights/tpet/"		
	adult = "adult=" + Adults + "&"
	children = "children=" + childrenNumber + "&"
	adultsv2 = "adultsv2=" + adultsNumber + "&"	
	infants = "infants=" + infantsNumber + "&"
	end = "cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home"
	
	for i in range(len(ListAge)):
		message = message + ListAge[i] + "%7c"
	
	childrenv2 = "childrenv2=" + message + "&"
	
	if (TripType == "OW"):
		GoDate = GoDate + "?"
		URL = Index + GoDate + adult + children + adultsv2 + childrenv2 + infants + end
		#webView(URL)
	elif(TripType == "RT"):
		GoDate = GoDate + "/"
		BackDate = BackDate + "?"
		URL = Index + GoDate + BackDate + adult + children + adultsv2 + childrenv2 + infants + end
		#webView(URL)


def getWorldwideName():
	Index = "https://www.skyscanner.com.tw/transport/flights-from/tpet/"
	Today = splitDate(datetime.now()) + "?"
	adult = "adult=1&"
	children = "children=0&"
	adultsv2 = "adultsv2=1&"
	childrenv2 = "childrenv2=&"
	infants = "infants=0&"
	end = "cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home"
	URL = Index + Today + adult + children + adultsv2 + childrenv2 + infants + end
	getJavaScript(URL)	

		
def getCountryName(CountryName):
	Index = "https://www.skyscanner.com.tw/transport/flights/tpet/"
	Country = CountryName + "/"
	Today = splitDate(datetime.now()) + "?"
	adult = "adult=1&"
	children = "children=0&"
	adultsv2 = "adultsv2=1&"
	childrenv2 = "childrenv2=&"
	infants = "infants=0&"
	end = "cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home"
	URL = Index  + Country + Today + adult + children + adultsv2 + childrenv2 + infants + end
	getJavaScript(URL)

	
def getJavaScript(url):
	#driver = webdriver.PhantomJS(executable_path = "C:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
	print (url)
	options = webdriver.ChromeOptions()
	options.add_argument('lang=zh-Hant-TW.UTF-8')
	options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"')
	#options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
	
	driver = webdriver.Chrome(executable_path = "C:/chromedriver.exe", chrome_options = options)	
	driver.set_page_load_timeout(30)
	#time.sleep(3)
	html = driver.get(url)
	#html = driver.get("https://www.skyscanner.com.tw/")
	#driver.add_cookie({'name':'userName','value':'youname'})
	#driver.add_cookie({'name':'uid','value':'54ef61ac-0a2d-44db-a1b3-6cbf34210ea5'})	
	
	driver.add_cookie({'name':'ASP.NET_SessionId','value':'96bcnigqd'})
	driver.add_cookie({'name':'DAPROPS','value':'"bjs.webGl:1|bjs.geoLocation:1|bjs.webSqlDatabase:1|bjs.indexedDB:1|bjs.webSockets:1|bjs.localStorage:1|bjs.sessionStorage:1|bjs.webWorkers:1|bjs.applicationCache:1|bjs.supportBasicJavaScript:1|bjs.modifyDom:1|bjs.modifyCss:1|bjs.supportEvents:1|bjs.supportEventListener:1|bjs.xhr:1|bjs.supportConsoleLog:1|bjs.json:1|bjs.deviceOrientation:0|bjs.deviceMotion:1|bjs.touchEvents:0|bjs.querySelector:1|bjs.battery:1|bhtml.canvas:1|bhtml.video:1|bhtml.audio:1|bhtml.svg:1|bhtml.inlinesvg:1|bcss.animations:1|bcss.columns:1|bcss.transforms:1|bcss.transitions:1|idisplayColorDepth:24|bcookieSupport:1|sdevicePixelRatio:1.25|sdeviceAspectRatio:16/9|bflashCapable:0|baccessDom:1|buserMedia:1"'})
	driver.add_cookie({'name':'RT','value':'"dm=skyscanner.com.tw&si=0237398f-1265-4c38-a3aa-c3d5a63009b1&ss=1524018744292&sl=3&tt=8645&obo=0&sh=1524019105759%3D3%3A0%3A8645%2C1524018885462%3D2%3A0%3A6100%2C1524018746731%3D1%3A0%3A2419&bcn=%2F%2F36fb61b0.akstat.io%2F&ld=1524019105759&r=https%3A%2F%2Fwww.skyscanner.com.tw%2Ftransport%2Fflights-from%2Ftpet%2F180418%3Fcdd62763e2ade5d8ee7b3f302586ff71&ul=1524019213620"'})
	driver.add_cookie({'name':'X-Mapping-fpkkgdlh','value':'402D944B5CC61C46E602D3B5E8CB7993'})
	driver.add_cookie({'name':'X-Mapping-gfnkmhhl','value':'D4939D9814284B265C9DB9A4F11CD396'})
	driver.add_cookie({'name':'X-Mapping-gfnniahc','value':'88B6FC8A591734A705679F5306110A76'})
	driver.add_cookie({'name':'X-Mapping-rrsqbjcb','value':'n585oyq9u4p7nk2fv507dsrhhi1pltmx'})
	driver.add_cookie({'name':'__gads','value':'ID=4f802f4e97899153:T=1523960447:S=ALNI_MbhU_wpUSfyPRdmvmySlmmwOnHeMA'})
	driver.add_cookie({'name':'_ga','value':'GA1.3.250470981.1523960449'})
	driver.add_cookie({'name':'_gat','value':'1'})
	driver.add_cookie({'name':'_gat_uatracker','value':'1'})
	driver.add_cookie({'name':'_gid','value':'GA1.3.343558848.1523960449'})
	driver.add_cookie({'name':'abgroup','value':'23928338'})
	driver.add_cookie({'name':'acq','value':'263356c3-e647-4d14-b142-b62b9ee31c77|263356c3-e647-4d14-b142-b62b9ee31c77'})
	driver.add_cookie({'name':'akaas_flights-home','value':'1526616221~rv=1~id=8413a0822de6b26792c6eef18451ec85'})
	driver.add_cookie({'name':'cto_lwid','value':'14a46e9f-cbfd-4cb2-81e5-24229b9d81c4'})
	driver.add_cookie({'name':'firstvisit','value':'overlay:::show'})
	driver.add_cookie({'name':'mp_2434748954c30ccc5017faa456fa3d38_mixpanel','value':'%7B%22distinct_id%22%3A%20%22162d31f07a454f-04aecfd6fa4411-b34356b-144000-162d31f07a64c3%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22User%20Locale%22%3A%20%22ZH-TW%22%2C%22User%20Market%22%3A%20%22TW%22%2C%22User%20Currency%22%3A%20%22TWD%22%2C%22New%20User%22%3A%20false%2C%22Internal%20User%22%3A%20%22%22%2C%22Mobile%22%3A%20%22FALSE%22%2C%22Tablet%22%3A%20%22FALSE%22%2C%22OS%20Version%22%3A%20%22NT%2010.0%22%2C%22Device%20Model%22%3A%20%22CHROME%20-%20WINDOWS%22%2C%22Browser%20Version%22%3A%20%2265.0.3325.181%22%2C%22Microsite%22%3A%20%22%22%2C%22Cookie%20Policy%20Alert%20Acknowledged%22%3A%20false%7D'})
	driver.add_cookie({'name':'preferences','value':'d3774037b1914b3f99a275b7f817ab12'})
	driver.add_cookie({'name':'scanner','value':'adults:::1&originalAdults:::1&adultsV2:::1&children:::0&originalChildren:::0&infants:::0&originalInfants:::0&charttype:::1&rtn:::true&preferDirects:::false&includeOnePlusStops:::true&cabinclass:::Economy&tripType:::OneWayTrip&ncr:::false&lang:::ZW&currency:::TWD&outboundAlts:::false&inboundAlts:::false&from:::TPET&oym:::1804&oday:::18&usrplace:::TW&wy:::0&to:::&iym:::&iday:::&fromCy:::TW&toCy:::'})
	driver.add_cookie({'name':'settings','value':'acql:::true'})
	driver.add_cookie({'name':'ssab','value':'Ads_UseESIAds_V1:::b&fps_route_summary_traffic_shift_V6:::b&new_price_alerts_ui_V2:::b&fps_lus_qss_automatic_rules_V19:::a&fps_mbmd_V11:::b&mag_mashups_V6:::b&fbw_enable_payment_billing_review_V14:::a&UtidTravellerIdentity_V11:::b&Car_AATest_V4:::b&fbw_braintree_new_cvv_service_V6:::b&appinsp_VES_USE_BROWSE_PROXY_V4:::on&glu_springCleanRollout_V2:::a&WPT_SaddlebagJs_V30:::b&dbook_flot_trafficcontrol_V12:::a&JV_LavelPrice_EnableforJPmarket_24_02_2017_19_49_V1:::b&WPT_React16_upgrade_V2:::b&fbw_remove_footer_V2:::a&TripsTopicPage_Hidethetopicpage_27_02_2018_34_33_V1:::a&skippy_website_link_service_integration_V23:::b&dbook_cath_trafficcontrol_all_web_V2:::a&Hfe_OfficialPartner_It2_V2:::b&scaffold_wireup_dont_delete_V1:::a&Tss_ConductorDayviewProxy_V54:::b&FLUX_GDT2791_SendPriceTraceToMixpanel_V6:::b&Trex_OCSearchControls_V27:::b&HFE_NewReviewsWithSocial_V1:::a&fbw_auth_V26:::b&AAExperiment_V8:::a&fps_lus_send_quotes_to_slipstream_V25:::noexperiment&Fss_NewSearchControls_V6:::c&dbook_drag_trafficcontrol_all_web_V2:::a&CAKE_DealsWidget_DayviewCheapest_V1:::a&Hsc_MexicanToAS2_V4:::b&FLUX787_QuoteBlacklist_V2:::a&Hfe_PricePerNight_V2:::b&DEAL_Default_To_Two_Guests_V3:::b&fbw_auth_inline_V7:::b&Hsc_ChildrenAgeView_V10:::b&Fss_springclean_datepicker_V5:::b&rts_magpie_soow_data_collection_V4:::budgetscheduled&TurnFeatureTests:::on&Web_Migration_home_V4:::c&dbook_sune_trafficcontrol_web_V3:::a&TCS_Send_Searching_Email_V4:::b'})
	driver.add_cookie({'name':'ssassociate','value':''})
	driver.add_cookie({'name':'ssculture','value':'locale:::zh-TW&currency:::TWD&market:::TW'})
	driver.add_cookie({'name':'sspref','value':'authcheckedexpiry:::1524029248210'})	
	driver.add_cookie({'name':'traveller_context','value':'b7cbe336-593d-46cc-b165-bc5f58248754'})
	driver.add_cookie({'name':'ver','value':'28'})
	
	
	time.sleep(2)
	driver.find_element_by_xpath("//*[@id=\"js-destination-input\"]").send_keys("世界各地")
	#//*[@id="destination-fsc-search"]
	
	time.sleep(1)
	driver.find_element_by_xpath("//*[@id=\"js-search-controls-container\"]/form/section[2]/button").click()	
	time.sleep(1)
	
	time.sleep(60)
	html = driver.page_source
	soup = BeautifulSoup(html, 'lxml')	
	name_box = soup.find_all("div", attrs={"class": "Destination-1vPQi"})	
	#Destination-1vPQi
	print (name_box)
	'''
	try:	
		headers = requests.utils.default_headers()
		headers.update(
			{
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
			}	
		)
		response = requests.get(URL, headers=headers)		
		content = response.text.encode('utf8')
		with open("html.txt", "w+") as Result:			
			Result.write(str(content))
					
				
		soup = BeautifulSoup(content, 'lxml')		
		#name_box = soup.find_all("div", attrs={"class": "browse-data-route"})		
	except Exception as e:
		print ("網址錯誤")
		print (e)
	'''	
def SearchLocation():
	print("只有地方提供顯示晚整票價服務")
	Destination = input(">>>請輸入想要查詢的地方 (1)世界各地 (2)國家(地方)")
	if (Destination == '1'):
		getWorldwideName()
	elif (Destination == '2'):
		Country = input(">>>請輸入想要查詢的國家(地方) (注. 需要知道確切的國家(地方)在SkyScanner的簡寫名稱)")
		getCountryName(Country)
	
if __name__ == '__main__':
	print ("**************************************")
	print ("*                                    *")
	print ("*          歡迎使用訂票程式          *")
	print ("*                                    *")
	print ("**************************************")
	type = input("請輸入想使用的功能 (1)查詢地點與票價 (2)快速訂票 :")
	if (type == '1'):
		SearchLocation()
	elif(type == '2'):
		Booting()
	