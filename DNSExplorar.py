#!/user/bin/python3
from os import linesep
import dns
import dns.resolver
import socket
import sys
# import threading
# import concurrent.futures

def ReverseDNS(ip):
    """ Gets the host name/s associated with an IP address """
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]]+result[1]
    except socket.herror:
        return None

def DNSRequest(domain):
    """ Gets the IP on a given sub/domain """
    try:
        result = dns.resolver.resolve(domain)
        if result:
            if domain not in Domains:
                Domains.append(domain)
            for answer in result:
                if str(answer) not in IPs:
                    IPs.append(str(answer))
                print(domain+":::"+str(answer))
                Domain_Name = ReverseDNS(answer.to_text())
                if Domain_Name not in Domain_Names:
                    Domain_Names.append(Domain_Name)
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []

def SubdomainSearch(domain, subs,nums):
    """ performs a dictionarry subdomain enumeration on a given domain to get subdomains with their associated IPs """
    for word in subs:
        print("{}%\r".format(int(subs.index(word)/len(subs)*100)),end="")
        subdomain = word+"."+domain
        DNSRequest(subdomain)
        if nums:
            for i in range(0,10):
                s = word+str(i)+"."+domain
                DNSRequest(s)

var = sys.argv[1:]
if "-h" in var:
    print("USAGE:   python DNSExploration.py -d [Domain] -w [Subdomains_File] [--find-once]",linesep)
    exit()
if "-d" in var:
    domain = var[var.index("-d")+1]
if "-w" in var:
    Subs_Wordlist = var[var.index("-w")+1]
count = True
if "--find-once" in var:
    count = False
IPs = []
Domains = []
Domain_Names = []
# x = 0

with open(Subs_Wordlist,"r") as f:
    subs = f.read().splitlines()
SubdomainSearch(domain,subs,count)

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
