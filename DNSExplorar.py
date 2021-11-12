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
        subdomain = word+"."+domain
        DNSRequest(subdomain)
        if nums:
            for i in range(0,10):
                s = word+str(i)+"."+domain
                DNSRequest(s)

print("USAGE:   python DNSExploration.py [Domain] [Subdomains_File]",linesep)
domain = sys.argv[1]
Subs_Wordlist = sys .argv[2]
IPs = []
Domains = []
Domain_Names = []
# x = 0

with open(Subs_Wordlist,"r") as f:
    subs = f.read().splitlines()
SubdomainSearch(domain,subs,True)

# with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#     executor.map(SubdomainSearch(domain,subs,True), range(sys.sys.argv[3]))

print()
print("IPs Found:")
for i in IPs:
    print(i)
print("-----------------------------")
print("Domains Found:")
for d in Domains:
    print(d)
print("-----------------------------")
print("Domain Names Found:")
for dn in Domain_Names:
    if dn != None:
        print(dn)