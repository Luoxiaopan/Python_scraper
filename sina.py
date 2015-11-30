import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

myHeaders = {}
myHeaders["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0"
myHeaders["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

def loginMicroblog():
	global myHeaders
	login_url = "http://login.weibo.cn/login/"
	print("====> The login_url: " + login_url)
	print("====> Visit login_url... ")
	login_reponse = requests.get(login_url,headers = myHeaders)
	bsObj = BeautifulSoup(login_reponse.text,"lxml")
	action_url = bsObj.find("form").attrs["action"]
	action_url = login_url + action_url
	print("====> The action_url: " + action_url)
	print("====> Visit action_url... ")
	submit_dict = {}
	input_values = bsObj.find("form").findAll("input")
	for in_value in input_values:
		if "name" in in_value.attrs:
			if "value" in in_value.attrs:
				submit_dict[in_value.attrs["name"]] = in_value.attrs["value"]
			else:
				submit_dict[in_value.attrs["name"]] = ""
			if re.match(r"password.*",in_value.attrs["name"]):
				submit_dict[in_value.attrs["name"]] = "@123132123luo"
			if in_value.attrs["name"] == "remember":
				submit_dict[in_value.attrs["name"]] = "on"
			if in_value.attrs["name"] == "mobile":
				submit_dict[in_value.attrs["name"]] = "15861815928"
	session = requests.Session()
	s = session.post(action_url,params = submit_dict,headers = myHeaders)
	print("Login Success")
	parseMicroBlog(s.text)

def parseMicroBlog(text):
	profile_bsObj = BeautifulSoup(text,"lxml")
	microblogs = profile_bsObj.findAll("div",id = re.compile("M_.*"))
	for microblog in microblogs:
		print("--------------")
		divs = microblog.findAll("div")
		#0
		profile_url = divs[0].find("a",{"class":"nk"}).attrs["href"]
		profile_name = divs[0].find("a",{"class":"nk"}).get_text()
		microblog_content = divs[0].find("span",{"class":"ctt"}).get_text()
		if divs[0].find("span",{"class":"cmt"}) is not None:
			forward_url = divs[0].find("span",{"class":"cmt"}).find("a").attrs["href"]
			forward_name = divs[0].find("span",{"class":"cmt"}).find("a").get_text()
			print(forward_url)
			print(forward_name)
		print(profile_url)
		print(profile_name)
		print(microblog_content)
		
		praise_url = microblog.find("a",href=re.compile("^http://weibo\.cn/attitude/.*$"))
		comment_url = microblog.find("a",{"class":"cc"},href=re.compile("^http://weibo\.cn/comment/.*$"))
		print(praise_url)
		print(comment_url)


			


def postMicroblog(content):
	global myHeaders
	s = session.get("http://weibo.cn/")
	submit_url = BeautifulSoup(s.text,"lxml").find("form",action = re.compile("/mblog/sendmblog\?st=.*")).attrs["action"]
	weibo_content = {"rl":"0"}
	weibo_content["content"] = content
	s = session.post("http://weibo.cn/"+submit_url,params = weibo_content,headers = myHeaders)

loginMicroblog()



# myHeaders["Accept-Encoding"] = "gzip, deflate"
# myHeaders["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
# myHeaders["Connection"] = "keep-alive"
# myHeaders["Host"] = "login.weibo.cn"
# myHeaders = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}


# login_url = "http://login.weibo.cn/login/"
# print("====> The login_url: " + login_url)
# print("====> Visit login_url: ")
# login_reponse = requests.get(login_url,headers = myHeaders)
# bsObj = BeautifulSoup(login_reponse.text,"lxml")


# action_url = bsObj.find("form").attrs["action"]
# action_url = "http://login.weibo.cn/login/" + action_url
# print("====> The action_url: " + action_url)
# print("====> Visit action_url: ")
# submit_dict = {}
# input_values = bsObj.find("form").findAll("input")
# for in_value in input_values:
# 	if "name" in in_value.attrs:
# 		if "value" in in_value.attrs:
# 			submit_dict[in_value.attrs["name"]] = in_value.attrs["value"]
# 		else:
# 			submit_dict[in_value.attrs["name"]] = ""
# 		if re.match(r"password.*",in_value.attrs["name"]):
# 			submit_dict[in_value.attrs["name"]] = "@123132123luo"
# 		if in_value.attrs["name"] == "remember":
# 			submit_dict[in_value.attrs["name"]] = "on"
# 		if in_value.attrs["name"] == "mobile":
# 			submit_dict[in_value.attrs["name"]] = "15861815928"

# session = requests.Session()
# s = session.post(action_url,params = submit_dict,headers = myHeaders)
# s = session.get("http://weibo.cn/")
# submit_url = BeautifulSoup(s.text,"lxml").find("form",action = re.compile("/mblog/sendmblog\?st=.*")).attrs["action"]
# submit_dict = {"content":"test","rl":"0"}
# s = session.post("http://weibo.cn/"+submit_url,params = submit_dict,headers = myHeaders)

# print(s.text)

