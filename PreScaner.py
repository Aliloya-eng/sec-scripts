import sys
import os

vars = sys.argv[1:]
url = vars[vars.index("-url")+1]
domain = vars[vars.index("-domain")+1]

# DOMAIN
## whois
print("whois-ing")
os.system("whois {} > {}/whois.txt".format(domain,domain))
## dig
print("dig-ing")
os.system("dig {} > {}/dig.txt".format(domain,domain))
## dnsrecon
print("dnsrecon-ing")
os.system("dnsrecon -d {} -a -s -b -y -k -w -z -t std > {}/dnsrecon.std.txt".format(domain,domain))
os.system("dnsrecon -d {} -a -s -b -y -k -w -z -t crt > {}/dnsrecon.crt.txt".format(domain,domain))
## sublister
print("sublister-ing")
os.system("sublist3r -d {} -v > {}/sublist3r.txt".format(domain,domain))
## theHarvester
print("theHarvester-ing")
os.system("theHarvester -d {} -g -s -r -n -b all > {}/theHarvester.txt".format(domain,domain))

# URL
## whatweb
print("whatweb-ing")
os.system("whatweb -a 3 -v {} > {}/whatweb.txt".format(url,domain))
## nikto
print("whatweb-ing")
os.system("nikto -host {} > {}/nikto.txt".format(url,domain))
