#!/user/bin/python3
import sys
import os

vars = sys.argv[1:]
if "-h" in vars:
    print('''
    PreScanner is a script written in Python3 to automate some of the basic recon processes. It simply calls other tools and prints the outout into text files in a subdirectory that holds the name of the examined domain.
    Usage example:   python PreScanner.py -url http://sub1.sub2.target.test/ -domain sub2.target.test --A     (python3)
    
    Target
        -url        the URL of the target
        -domain     the domain of the target
    Coverage
        --A         exclude active(url) scans
        --P         exclude passive(domain) scans
        --O         overwrite previous scans (for domain scans only, url scans are overwritten anyway if not excluded)
    ''')
    exit()

if  "-url" not in vars or "-domain" not in vars:
    print('''
    Please enter the url and the domain of the target
    Usage example:   python PreScanner.py -url http://sub1.sub2.target.test/ -domain sub2.target.test     (python3)
    ''')
    exit()

url = vars[vars.index("-url")+1]
url = url.replace("https","http")
domain = vars[vars.index("-domain")+1]
passive = "--P" not in vars
active = "--A" not in vars
overwrite = "--O" in vars

if passive:
    if overwrite or not os.path.isdir(domain):
        # DOMAIN - PASSIVE
        os.system("mkdir {}".format(domain))
        ## whois
        print("whois-ing")
        os.system("whois {} > {}/whois.txt".format(domain,domain))
        ## dig
        print("dig-ing")
        os.system("dig {} > {}/dig.txt".format(domain,domain))
        ## dnsrecon
        print("dnsrecon-ing")
        # os.system("dnsrecon -d {} -a -s -b -y -k -w -z -t std > {}/dnsrecon.std.txt".format(domain,domain))
        os.system("dnsrecon -d {} -a -s -b -y -k -w -z -t crt > {}/dnsrecon.crt.txt".format(domain,domain))
        ## sublister
        print("sublister-ing")
        os.system("sublist3r -d {} -v > {}/sublist3r.txt".format(domain,domain))
        ## theHarvester
        print("theHarvester-ing")
        os.system("theHarvester -d {} -g -s -r -b all > {}/theHarvester.txt".format(domain,domain))

if active:
    # URL - ACTIVE
    ## whatweb
    print("whatweb-ing")
    os.system("whatweb -a 3 -v {} > {}/whatweb-{}.txt".format(url,domain,url.replace("/","+")))
    ## nikto
    print("Nikto-ing")
    os.system("nikto -host {} -timeout 60 > {}/nikto-{}.txt".format(url,domain,url.replace("/","+")))
