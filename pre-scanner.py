#!/user/bin/python3
from base64 import urlsafe_b64decode
from genericpath import exists
import sys
import os
import re

vars = sys.argv[1:]
if "-h" in vars:
    print('''
    pre-scanner is a script written in Python3 to automate some of the basic recon processes.
    It simply calls other tools and prints the output into text files in a subdirectory that holds the name of the examined domain.

    Target
        -u          the URL of the target, or a file comtaining list of urls
        -d          the domain of the target, or a file containing list of domains
    Coverage
        --A         exclude active(url) scans
        --P         exclude passive(domain) scans
        --O         overwrite previous scans (for domain scans only, url scans are overwritten anyway if not excluded)

    Usage example:   python pre-scanner.py -u http://sub1.sub2.target.test/ -d sub2.target.test --A         
    ''')
    exit()

if  "-u" not in vars and "-d" not in vars:
    print('''
    Please enter the url (-u) and the domain (-d) of the target (-h for help)
    Usage example:   python pre-scanner.py -u http://sub1.sub2.target.test/ -d sub2.target.test     (python3)
    ''')
    exit()

passive = not ("--P" in vars or "-d" not in vars)
active = not ("--A" in vars or "-u" not in vars)
overwrite = "--O" in vars

if "-u" in vars:
    u = vars[vars.index("-u")+1]
    urls=[]
    if exists(u):
        with open(u,"r") as f:
            for l in f:
                urls.append(l.strip())
    else:
        urls=[u.strip()]

if "-d" in vars:
    d = vars[vars.index("-d")+1]
    domains=[]
    if exists(d):
        with open(d,"r") as f:
            for l in f:
                domains.append(l.strip())
    else:
        domains=[d.strip()]

if not exists("OUT"):
    os.system("mkdir OUT")

print('''
We will do some scans for you. Other tools that we suggest you visit yourself are:
- wappalyzer
- Recon-ng
- https://www.ssllabs.com/ssltest/
- https://www.netcraft.com/
- https://dnsdumpster.com/
- https://www.shodan.io/
- https://haveibeenpwned.com/
- https://breachchecker.com/
- https://osintframework.com/
...
..
.
''')

if passive:
    for domain in domains:
        if overwrite or not os.path.isdir(domain):
            # DOMAIN - PASSIVE
            if not exists("OUT/"+domain):
                os.system("mkdir OUT/{}".format(domain))
            ## whois
            print("whois {} > OUT/{}/whois.txt".format(domain,domain))
            os.system("whois {} > OUT/{}/whois.txt".format(domain,domain))
            ## host
            print("host -a {} > OUT/{}/host.txt".format(domain,domain))
            os.system("host -a {} > OUT/{}/host.txt".format(domain,domain))
            ## dnsrecon
            print("dnsrecon -d {} -a -s -b -y -k -w -z -t crt > OUT/{}/dnsrecon.crt.txt".format(domain,domain))
            os.system("dnsrecon -d {} -a -s -b -y -k -w -z -t crt > OUT/{}/dnsrecon.crt.txt".format(domain,domain))
            # os.system("dnsrecon -d {} -a -s -b -y -k -w -z -t std > {}/dnsrecon.std.txt".format(domain,domain))
            ## sublister
            print("sublist3r -d {} -v > OUT/{}/sublist3r.txt".format(domain,domain))
            os.system("sublist3r -d {} -v > OUT/{}/sublist3r.txt".format(domain,domain))
            ## theHarvester
            print("theHarvester -d {} -g -s -r -b all > OUT/{}/theHarvester.txt".format(domain,domain))
            os.system("theHarvester -d {} -g -s -r -b all > OUT/{}/theHarvester.txt".format(domain,domain))
            ## dns-explorar
            print("python(3) dns-explorar.py -d {} -w subdomains.txt > OUT/{}/dns-explorar.txt".format(domain,domain))
            if not exists("dns-explorar.py"):
                print(" --- DNSEplorar is not installed in this directory, if you want to use this tool please download it in the same directory with 'wget https://raw.githubusercontent.com/Aliloya-eng/sec-scripts/main/dns-explorar.py' --- ")
            if not exists("subdomains.txt"):
                print(" --- No 'subdomain.txt' wordlist was found to use the dns-explorar tool, if you want to use this tool please put the subdomains wordlist in the same directory under the name subdomains.txt --- ")
            if exists("dns-explorar.py") and exists("subdomains.txt"):
                os.system("python3 dns-explorar.py -d {} -w subdomains.txt > OUT/{}/dns-explorar.txt".format(domain,domain))
                os.system("python dns-explorar.py -d {} -w subdomains.txt > OUT/{}/dns-explorar.txt".format(domain,domain))

if active:
    for url in urls:
        out_name = url.removeprefix("http://").removeprefix("https://").replace("/","+")
        if "-d" in vars:
            for domain in domains:
                if domain in url:
                    out_name = domain
        # URL - ACTIVE
        if not exists(out_name):
            os.system("mkdir OUT/{}".format(out_name))
        ## nmap
        target = re.search("\/\/(.*)\/",url)
        print(target)[0]
        print("nmap -T4 -p80,443,8080 -A -v --script http* {} > OUT/{}/nmap.txt".format(target,out_name))
        os.system("nmap -T4 -p80,443,8080 -A -v --script http* {} > OUT/{}/nmap.txt".format(target,out_name))
        ## whatweb
        print("whatweb -a 3 -v {} > OUT/{}/whatweb.txt".format(url,out_name))
        os.system("whatweb -a 3 -v {} > OUT/{}/whatweb.txt".format(url,out_name))
        ## nikto
        print("nikto -host {} -timeout 60 > OUT/{}/nikto.txt".format(url,out_name))
        os.system("nikto -host {} -timeout 60 > OUT/{}/nikto.txt".format(url,out_name))
        
