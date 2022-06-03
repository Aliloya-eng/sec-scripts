#!/user/bin/python3
from os import linesep
import dns
import dns.resolver
import socket
import sys

from pyparsing import empty
# import threading
# import concurrent.futures

def ReverseDNS(ip):
    """ Gets the host name/s associated with an IP address """
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]]+result[1]
    except socket.herror:
        return None

def DNSRequest(domain, i):
    """ Gets the IP on a given sub/domain """
    try:
        result = dns.resolver.resolve(domain)
        if result:
            Domains[i+1].append(domain)
            for answer in result:
                if str(answer) not in IPs:
                    IPs.append(str(answer))
                print(domain+":::"+str(answer)+"                   ")
                Domain_Name = ReverseDNS(answer.to_text())
                if Domain_Name not in Domain_Names:
                    Domain_Names.append(Domain_Name)
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []

def SubdomainSearch(domain, subs, nums, i):
    """ performs a dictionarry subdomain enumeration on a given domain to get subdomains with their associated IPs """
    for word in subs:
        print("Depth level ({}) : {} / {} = {}%                    \r".format(i+1,(len(subs)*(Domains[i].index(domain)))+subs.index(word),len(subs)*len(Domains[i]),int(100*(((len(subs)*(Domains[i].index(domain)))+subs.index(word))/(len(subs)*len(Domains[i]))))),end="")
        subdomain = word+"."+domain
        DNSRequest(subdomain, i)
        if nums:
            for j in range(0,10):
                s = word+str(j)+"."+domain
                DNSRequest(s,i)

var = sys.argv[1:]
if "-h" in var:
    print("USAGE:   python dns-exploration.py -d [Domain] -w [Subdomains_File] [--find-once]",linesep)
    exit()
if "-d" in var:
    domain = var[var.index("-d")+1]
else:
    print("please use -d to provide the target domain")
    exit()
if "-w" in var:
    Subs_Wordlist = var[var.index("-w")+1]
else:
    print("please use -w to provide a sundomains wordlist")
    exit()
count = True
if "--find-once" in var:
    count = False
IPs = []
Domains=[[domain]]
Domain_Names = []
# x = 0

with open(Subs_Wordlist,"r") as f:
    subs = f.read().splitlines()

for i in range(3):
    Domains.append([])
    for d in Domains[i]:
        SubdomainSearch(d,subs,count,i)
if len(Domains[3]) > 0:
    print("level 3 of subdomains is not empty, if you want to discover further subdomains with deeper levels please provide the level 3 domains found in the output back as input to the tool manually and run it against them")
Domains = list(Domains[0]+Domains[1]+Domains[2]+Domains[3])    

# with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#     executor.map(SubdomainSearch(domain,subs,True), range(sys.sys.argv[3]))

print("--------------------------------------------------------")
print('''***************** IPs Found: *****************''')
for i in IPs:
    print(i)
print('''*************** Domains Found: ***************''')
for d in Domains:
    print(d)
print('''************ Domains Names Found: ************''')
for dn in Domain_Names:
    if dn != None:
        print(dn)
print("--------------------------------------------------------")
print("--------------------------------------------------------")
