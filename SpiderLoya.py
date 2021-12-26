# Welcome to SpiderLoya by Ali.W.Hassan. Please use it only for ethical purposes
# This script is currently under test - I would appreciate any advice/feedback/test results
# For test results please provide the command used along with the output received and any extra information/suggestions
# Contact Email: alihassan.courses@gmail.com

#!/usr/bin/python3
import re
from requests import get
from urllib.parse import unquote
import sys
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def random_agent(user_agent):
    '''Switch the user-agent header randomly from a file you provide - takes a list of user-agents'''
    if len(user_agent)==1:
        return user_agent[0]
    r = int(random(len(user_agent)-1))
    return user_agent[r]
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def random_proxy(proxy):
    '''Switch the proxy randomly from a file you provide - takes a list of proxy values'''
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
    '''Sends a GET request to the target url and returns the HTTP response body - takes a string url'''
    headers["user-agent"] = random_agent(user_agent)
    if url[-4:]==".exe":
        print("//////////////////////////////// Error: Link {} skipped - ending with .exe".format(url))
        return ""
    if domain not in url:
        print("////////////////////////////////  ERROR: GETTING PAGE OUT OF DOMAIN")
        return ""
    if random_proxy==True:
        try:
            print("Getting >> {}".format(url))
            res = get(url, timeout=timeout, verify=verify,proxies=random_proxy(proxy),headers=headers)
        except requests.Timeout:
            print("Connection timeout - target {} didn't respond in time".format(url))
            return ""
    else:
        try:
            print("Getting >> {}".format(url))
            res = get(url, timeout=timeout, verify=verify,headers=headers)
        except requests.Timeout:
            print("Connection timeout - target {} didn't respond in time".format(url))
            return ""
    return res.text
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def Globalize(file_links, dir_links, http_links_in_scope, http_links_out_scope, other_links):
    '''Adding all links from Filter as final results - takes 5 lists'''
    global Global_Links
    filtered_dict={"files":file_links,"dirs":dir_links,"in":http_links_in_scope,"out":http_links_out_scope,"others":other_links}
    for k,v in filtered_dict.items():
        Global_Links[k] += v
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def link_filter(links,domain):
    '''Filters out the links found by the link extractor into 7 lists - takes a list of found links'''
    reg_dir = "^\S*$"
    reg_files = "\.+?\w+[\?\S]+$"
    links = list(set(links))

    exe = [item for item in links if item[-4:]==".exe"]

    http_links_out_scope = [item for item in links if "http" in item and domain not in item and item not in exe]
    http_links_in_scope = [item for item in links if "http" in item and domain in item and item not in exe ]
    
    in_domain_links = [item for item in links if "http" not in item and item not in exe]
    in_domain_links = list(set(in_domain_links))
    
    file_links = [item for item in in_domain_links if re.search(reg_files, item)]
    
    dir_links = [item for item in in_domain_links if  item not in file_links and re.search(reg_dir,item) and item !="\""]
    
    other_links = [item for item in in_domain_links if item not in dir_links and item not in file_links]

    Globalize(file_links, dir_links, http_links_in_scope, http_links_out_scope, other_links)
    return exe, file_links, dir_links, http_links_in_scope, http_links_out_scope, other_links, in_domain_links+http_links_in_scope
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def mail_finder(links_in_url):
    '''Extracts all mail addresses from a single web page - takes the body of a single http response'''
    mails = []
    reg_mails = ["mailto:(.*?)'","mailto:(.*?)\""]
    for link in links_in_url:
        page = get_page(link)
        for reg in reg_mails:
            mails += re.findall(reg,page)
    return list(set(mails))
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def link_extractor(link):
    '''Extracts all links/urls from a single web page - takes the body of a single http response'''
    found = []
    page = get_page(link)
    reg_link = "(?i)(src|href)[ ]?=[ ]?['|\"](\S+?)[\"|']"
    found += [unquote(item) for g1,item in re.findall(reg_link,page) if item != "" and item[0]!="#" and not "mailto" in item and not "callto" in item  and item not in Global_list]
    reg_full_link = "(?i)((https|http):\/\/\S+?)[\"|'|\ ]"
    found += [unquote(item) for item,g2 in re.findall(reg_full_link,page) if item != "" and item[0]!="#" and not "mailto" in item and not "callto" in item and item not in Global_list]
    global Global_list
    for i in found:
        if i not in Global_list:
            Global_list.append(i)
    return list(set(found))
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
def deep_extractor(link,depth,domain):
    '''Organises the found links with the help of the link filter and the globalizer and calls the links extractor for every link depending on the level of depth requested - takes a seed link, the level of depth, and the domain in scope'''
    prev = link
    for d in range(depth):
        print("////////////////////////////////////// layer {}".format(d+1))
        links = []
        print(">> {} Links Found:\n{}".format(len(prev),prev))
        for l in prev:
            if "http" in l:
                if domain not in l:
                    print("/////////WARNING//////// link skipped: link {} out of domain {}".format(l,domain))
                else:
                    links += link_filter(link_extractor(l),domain)[-1]
            else:
                if l[0] != "/":
                    links += link_filter(link_extractor(target_url+l),domain)[-1]
                else:
                    links += link_filter(link_extractor(target_url+l[1:]),domain)[-1]
        prev = links
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":

    # Reading command arguments
    var = sys.argv
    if "-h" in var or len(var)==1:
        print('''
           *******************
Welcome to *** SpiderLoya *** the customizable WebScraber
           *******************
# Welcome to SpiderLoya by Ali.W.Hassan. Please use it only for ethical purposes
# This script is currently under test - I would appreciate any advice/feedback/test results
# For test results please provide the command used along with the output received and any extra information/suggestions
# Contact Email: alihassan.courses@gmail.com

    -h              help
    -url            target url - please use the form: http://example.smth/
    -domain         domain in scope - single domain at a time
    -depth          depth of scraping - how many levels to go deep after each link found
    -timeout        timeout for each request (in seconds)
    -user-agent     user agent list as text file (one agent in each line)
    -proxy          proxies list as text file (one proxy in each line): 127.0.0.1:8080
    -headers        headers to be added (except user-agent) - in dictionarry form: {header1:value,header2:value,header3:value...}
        ''')
    else:
        if "-url" not in var:
            print("no url target specified, Please include a single url as: -url http://example.com/")
            exit()
        target_url = var[var.index("-url")+1]
        user_agent = ["SpiderLoya"]
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
            domain = var[var.index("-domain")+1][0]

        # setting up parameters and variables
        target = [target_url]
        Global_Links = {"files":[],"dirs":[],"in":target,"out":[],"others":[]}
        Global_list = target
        verify = False

        # Scraping
        deep_extractor([target_url],depth,domain)

        # Printing Results
        print('''
        ******************************
        ************RESULT************
        ******************************
        ''')
        print("All {} Links Found:".format(len(Global_list)))
        for i in Global_list:
            print(i)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////
