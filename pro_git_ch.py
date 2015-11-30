from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote,unquote
from bs4 import BeautifulSoup
import re
import os

urls_history_set = set()
urls_wait_open_list = []
base_url = "http://git.oschina.net/progit/"

#test
def downloadDirectory(absolute_url,base_url,save_directory):
	save_path = absolute_url.replace(base_url,"")
	save_path = save_directory + save_path
	if re.match(".*(%\w\w)+",save_path):
		save_path = unquote(save_path)
	directory = os.path.dirname(save_path)
	if not os.path.exists(directory):
		os.makedirs(directory)
	print(save_path + " saved at " + directory)
	return save_path

def retrivePages(start_url,download_dir):
	global urls_history_set
	global urls_wait_open_list
	global base_url
	urls_wait_open_list.append(start_url)
	while len(urls_wait_open_list) > 0:
		open_url = str(urls_wait_open_list.pop(0))
		if open_url not in urls_history_set:
			print("-------------")
			print("Visit " + open_url)
			html = urlopen(open_url)
			urls_history_set.add(open_url)
			urlretrieve(open_url,downloadDirectory(open_url,base_url,download_dir))
			bsObj = BeautifulSoup(html,"lxml")

			imgs = bsObj.findAll("img")
			for img in imgs:
				img_url = img.attrs["src"]
				img_url = base_url + img_url
				urlretrieve(img_url,downloadDirectory(img_url,base_url,download_dir))

			csses = bsObj.findAll("link",href=re.compile(".*\.css"))
			for css in csses:
				css_url = css.attrs["href"]
				css_url = base_url + css_url
				urlretrieve(css_url,downloadDirectory(css_url,base_url,download_dir))

			jses = bsObj.findAll("script",src=re.compile(".*\.js"))
			for js in jses:
				js_url = js.attrs["src"]
				js_url = base_url + js_url
				urlretrieve(js_url,downloadDirectory(js_url,base_url,download_dir))

			urls = bsObj.findAll("a",href = re.compile("^.*\.html$"))
			for url in urls:
				url_href = url.attrs["href"]
				#The url including Chinese should be qute.
				if re.match(r".*[\u4E00-\u9FA5]+",url_href):
					url_href = quote(url_href)
				#The relative path should be converted to absolute path
				if re.match(r"(?!http:).*\.html",url_href):
					url_href = base_url + url_href
				#Add the inner website which didn't be opened yet into the set.
				if url_href not in urls_history_set:
					if re.match(r"http://git\.oschina\.net/progit/.*\.html",url_href):
						urls_wait_open_list.append(url_href)

retrivePages("http://git.oschina.net/progit/index.html","/home/lxp/pro_git/")