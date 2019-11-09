# SkyScanner Analysis 2018
 分析SkyScanner網頁，並試者進行自動化訂票(學校作業:失敗)
1. 分析SkyScanner的網址規則，並製作出相對應的網址
2. 利用urllib + BeautifulSoup(失敗):
	1. urllib負責將網頁存取下來、BeautifulSoup將存取下來的網頁進行解析
	2. 即使加了正常瀏覽網頁時的user-agent仍會被擋下來
3. 利用requests + BeautifulSoup(失敗):
	1. requests加上user-agent能存取下來靜態網頁的部分，但仍擷取不到動態網頁
4. Selenium + chromedriver(失敗):
	1. SkyScanner會認瀏覽器的uuid，故導致用chromedriver會無法正常瀏覽skyscanner
	
	
	