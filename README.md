# My sec-scripts

This repo will be devoted to my scripted tools.<br>Most tools need a lot of testing, so I would be grateful for any feedback and contribution.<br>For test results please provide the command used along with the output received and any extra information/suggestions<br>Contact Email: alihassan.courses@gmail.com

### <u>DNSExplorar</u>
Performs a dictionary subdomain enumeration/bruteforce on a given domain to get subdomains with their associated IPs.
* USAGE:     `python DNSExploration.py [Domain] [Subdomains_File]`      (python3)
* example:   `python DNSExploration.py example.test line-separated-subdomains-wordlist.txt`
-------------------------------------------
### <u>PreScaner</u>
A simple enumeration tool that performs some basic scans (whois,whatweb,dig,dnsrecon,sublister,theHarvester,nikto) on a given url and a given domain, and prints the output into textfiles.
* USAGE:     `python PreScanner.py -url [URL] -domain [Domain]`         (python3)
* example:   `python PreScanner.py -url http://n1.example.test/ -domain example.test`
--------------------------------------------
### <u>ScraperLoya</u>
This tool is designed to read a web page and extract all links from it. Then, according to the provided depth, it will request each of the found links and look for links in the body of the responses.. and so on..
<br>
```
           *******************
Welcome to *** ScraperLoya *** the customizable WebScraber
           *******************

    -h              help
    -url            target url - please use the form: http://example.smth/
    -domain         domain in scope - single domain at a time
    -depth          depth of scraping - how many levels to go deep after each link found
    -timeout        timeout for each request (in seconds)
    -user-agent     user agent list as text file (one agent in each line)
    -proxy          proxies list as text file (one proxy in each line): 127.0.0.1:8080
    -headers        headers to be added (except user-agent) - in dictionary form: {header1:value,header2:value,header3:value...}
```

* USAGE:     `python ScraperLoya.py -url [URL] -domain [Domain] -depth [depth] -timeout [timeout] -user-agent [user-agent] -proxy [proxy] -headers [headers]`      (python3)
* example:   `python ScraperLoya.py -url http://n1.example.test/ -domain example.test -depth 3 -timeout 30 -user-agent userAgent-file.txt -proxy proxies-file.txt -headers {header1:value1,header2:value2,header3:value3}`
------------------------------------------
