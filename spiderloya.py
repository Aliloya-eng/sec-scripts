# Welcome to spiderloya by Ali.W.Hassan. Please use it only for ethical purposes
# This script is currently under test - I would appreciate any advice/feedback/test results
# For test results please provide the command used along with the output received and any extra information/suggestions
# Contact Email: alihassan.courses@gmail.com

# # Future improvements
# 1- Testing
# 2- Ignore links for different languages
# 3- ...


#!/usr/bin/python3
import re
from urllib.parse import unquote
import sys
import random
import requests
import time
from requests.api import get, head
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def is_web(url):
    '''Takes a string URL and returns:
    1- TRUE if the given URL is for a webpage
    2- FALSE for other types of files: image,pdf,css...'''
    ignore = ["pdf","png","jpg","gif","css","ttf","otf","woff","eot","svg","ttc","woff2","","","","","","","","",""]
    if str(url).split(".")[-1] in ignore:
        return False
    headers["user-agent"] = random_agent(user_agent)
    if random_proxy==True:
        try:
            res = head(url, timeout=timeout, verify=verify,proxies=random_proxy(proxy),headers=headers, allow_redirects=True)
        except requests.Timeout:
            print("Connection timeout - target {}".format(url))
            return False
    else:
        try:
            res = head(url, timeout=timeout, verify=verify,headers=headers, allow_redirects=True)
        except requests.Timeout:
            print("Connection timeout - target {}".format(url))
            return False
    if res.status_code in range(400,500):
        Global_400.append(url)
    elif res.status_code in range(500,600):
        Global_500.append(url)
    elif "html" in str(res.headers["content-type"]).lower():
        return True
    return False
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def wanted(l):
    '''Takes a string link and returns
    1- The link after standarizing it in the form of: target_url+sub-directory.
    2- TRUE if the link is a web page in scope
    3- FALSE if the link is not a web page or if it is out of scope'''
    if "http" in l:
        l = str(l).replace("https://","http://").strip()
        if not l.startswith(target_url) and not l.startswith("http://www."+str(target_url[7:])):
            if domain in l:
                Global_Skipped.append(l)
            return l,False
    else:
        if str(l).startswith("/"):
            l = target_url.strip()+l[1:]
        else:
            l = target_url.strip()+l
    return l,is_web(l)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def random_agent(user_agent):
    '''Takes a list of user-agents and switches the user-agent header randomly from the provided list'''
    if len(user_agent)==1:
        return user_agent[0]
    r = int(random(len(user_agent)-1))
    return user_agent[r]
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def random_proxy(proxy):
    '''Takes a list of proxy values and switch the proxy randomly from the provided list'''
    if len(proxy)<2:
        if len(proxy)==1:
            return {"http":proxy[0],"https":proxy[0]}
        else:
            return False
    r = int(random(len(proxy)-1))
    return {"http":proxy[r],"https":proxy[r]}
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def get_page(url):
    '''Takes a string url and sends a GET request to the target url and returns the HTTP response body'''
    headers["user-agent"] = random_agent(user_agent)
    if random_proxy==True:
        try:
            # print("Getting >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {}".format(url))
            res = get(url, timeout=timeout, verify=verify,proxies=random_proxy(proxy),headers=headers)
            Global_Gotten.append(url)
            return res.text
        except requests.Timeout:
            print("Connection timeout - target {}".format(url))
            return ""
    else:
        try:
            # print("Getting >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {}".format(url))
            res = get(url, timeout=timeout, verify=verify,headers=headers)
            Global_Gotten.append(url)
            return res.text
        except requests.Timeout:
            print("Connection timeout - target {}".format(url))
            return ""
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# def Globalize(file_links, dir_links, http_links_in_scope, http_links_out_scope, other_links):
#     '''Adding all links from Filter as final results - takes 5 lists'''
#     global Global_Links
#     filtered_dict={"files":file_links,"dirs":dir_links,"in":http_links_in_scope,"out":http_links_out_scope,"others":other_links}
#     for k,v in filtered_dict.items():
#         Global_Links[k] += v
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# def link_filter(links):
#     '''Filters out the links found by the link extractor into 7 lists - takes a list of found links'''
#     reg_dir = "^\S*$"
#     reg_files = "\.+?\w+[\?\S]+$"
#     links = list(set(links))

#     exe = [item for item in links if item[-4:]==".exe"]

#     http_links_out_scope = [item for item in links if "http" in item and domain not in item and item not in exe]
#     http_links_in_scope = [item for item in links if "http" in item and domain in item and item not in exe ]
    
#     in_domain_links = [item for item in links if "http" not in item and item not in exe]
#     in_domain_links = list(set(in_domain_links))
    
#     file_links = [item for item in in_domain_links if re.search(reg_files, item)]
    
#     dir_links = [item for item in in_domain_links if  item not in file_links and re.search(reg_dir,item) and item !="\""]
    
#     other_links = [item for item in in_domain_links if item not in dir_links and item not in file_links]

#     Globalize(file_links, dir_links, http_links_in_scope, http_links_out_scope, other_links)
#     return exe, file_links, dir_links, http_links_in_scope, http_links_out_scope, other_links, in_domain_links+http_links_in_scope
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# def mail_finder(links_in_url):
#     '''Extracts all mail addresses from a single web page - takes the body of a single http response'''
#     mails = []
#     reg_mails = ["mailto:(.*?)'","mailto:(.*?)\""]
#     for link in links_in_url:
#         page = get_page(link)
#         for reg in reg_mails:
#             mails += re.findall(reg,page)
#     return list(set(mails))
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def link_extractor(link):
    '''Takes a string URL and extracts all links/urls from its web page'''
    if link not in Global_Gotten:
        found = []
        page = get_page(link)
        reg_link = "(?i)(src|href)[ ]?=[ ]?['|\"](\S+?)[\"|']"
        found += [wanted(unquote(item))[0] for g1,item in re.findall(reg_link,page) if item != "" and item[0]!="#" and not "mailto" in item and not "callto" in item  and wanted(item)[1]]
        reg_full_link = "(?i)((https|http):\/\/\S+?)[\"|'|\ ]"
        found += [wanted(unquote(item))[0] for item,g2 in re.findall(reg_full_link,page) if item != "" and item[0]!="#" and not "mailto" in item and not "callto" in item and wanted(item)[1]]
        global Global_list
        # print("FOUND")
        for i in found:
            # print(str("{line: <150}".format(line=i)),end="\r")
            if i not in Global_list:
                Global_list.append(i)
        return list(set(found))
    else:
        return []
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def deep_extractor(link,depth):
    '''Takes a string link and an integer depth and makes a number of calls/branches, to the link_extractor, for every link depending on the depth requested'''
    prev = link
    for d in range(depth):
        print("////////////////////////////////////////////////////////////////// layer {}  ::::::  Number of links to be crawled = {}".format(d+1,len(prev)))
        # print(prev)
        links = []
        if len(prev)>0:
            for l in prev:
                links += link_extractor(l)
            prev = links
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    
    ts=time.time()
    # Reading command arguments
    var = sys.argv
    if "-h" in var or len(var)==1:
        print('''
           *******************
Welcome to *** spiderloya *** the customizable WebScraber
           *******************
# Welcome to spiderloya by Ali.W.Hassan. Please use it only for ethical purposes
# This script is currently under test - I would appreciate any advice/feedback/test results
# For test results please provide the command used along with the output received and any extra information/suggestions
# Contact Email: alihassan.courses@gmail.com

    -h              help
    -url            target url
    -domain         domain in scope - single domain at a time
    -depth          depth of scraping - how many levels to go deep after each link found = default 1
    -timeout        timeout for each request (in seconds) = default 30
    -user-agent     user agent list as text file (one agent in each line) = default spiderloya
    -proxy          proxies list as text file (one proxy in each line): 127.0.0.1:8080
    -headers        headers to be added (except user-agent) - in dictionarry form: {header1:value,header2:value,header3:value...}
        ''')
    else:
        if "-url" not in var:
            print("no url target specified, Please include a single url as: -url http://example.com/")
            exit()
        target_url = str(var[var.index("-url")+1]).replace("https","http")
        if target_url[-1] != "/":
            target_url = target_url+"/"
        user_agent = ["spiderloya"]
        if "-user-agent" in var:
            with open(var[var.index("-user-agent")+1]) as agents:
                user_agent = agents.readlines()
        proxy = []
        if "-proxy" in var:
            with open(var[var.index("-proxy")+1]) as proxies:
                proxy = proxies.readlines()
        depth = 1
        if "-depth" in var:
            depth = int(var[var.index("-depth")+1])
        timeout = 30
        if "-timeout" in var:
            timeout = int(var[var.index("-timeout")+1])
        headers = {}
        if "-headers" in var:
            headers.update(eval(var[var.index("-headers")+1]))
        reg_domain = "http[s]?:\/\/w{0,3}([\w.]+)\/?"
        domain = re.findall(reg_domain,target_url)[0]
        if "-domain" in var:
            domain = var[var.index("-domain")+1]

        # setting up parameters and variables
        target = [target_url]
        # Global_Links = {"files":[],"dirs":[],"in":target,"out":[],"others":[]}
        Global_list = target
        Global_Skipped = []
        Global_Gotten = []
        Global_400 = []
        Global_500 = []
        verify = False

        # Spidering
        deep_extractor([target_url],depth)

        # Printing Results
        print('''
        ******************************************************************************************
        ******************************************RESULT******************************************
        ******************************************************************************************
        
        ******************************************************************************************
            Links In Scope (sub-directories)
        ******************************************************************************************
        ''')        
        print("All {} Links Found:".format(len(Global_list)))
        for i in Global_list:
            print(i)
        print('''
        ******************************************************************************************
            Links With 400-like Error ---------- IGNORED
        ******************************************************************************************
        ''')
        print("All {} Links Responded with 400-500 Status Code:".format(len(Global_400)))
        for i in Global_400:
            print(i)
        print('''
        ******************************************************************************************
            Links With 500-like Error ---------- IGNORED
        ******************************************************************************************
        ''')
        print("All {} Links Responded with 500-600 Status Code:".format(len(Global_500)))
        for i in Global_500:
            print(i)
        print('''
        ******************************************************************************************
            Links OUT of Scope (other sub/domains) ---------- IGNORED
        ******************************************************************************************
        ''')
        print("All {} Links Skipped:".format(len(Global_Skipped)))
        for i in Global_Skipped:
            print(i)
    tf=time.time()
    print("total time: {}".format(tf-ts))
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
