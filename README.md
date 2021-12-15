# My sec-scripts
================
This repo will be devoted for my scripted tools. Most tools need alot of testing, so I would be grateful for any feedback and contribution.
For test results please provide the command used along with the output received and any extra information/suggestions
Contact Email: alihassan.courses@gmail.com

## DNSExplorar
Performs a dictionarry subdomain enumeration/bruteforce on a given domain to get subdomains with their associated IPs.
USAGE:     `python DNSExploration.py [Domain] [Subdomains_File]`      (python3)
example:   `python DNSExploration.py example.test line-seperated-subdomains-wordlist.txt`

## PreScaner
A simple enumeration tool that performs some basic scans (whois,whatweb,dig,dnsrecon,sublister,theHarvester,nikto) on a given url and a given domain, and prints the output into textfiles.
USAGE:     `python PreScanner.py -url [URL] -domain [Domain]`         (python3)
example:   `python PreScanner.py -url http://n1.example.test/ -domain example.test`

## ScraperLoya
This tool is desiegned to read a web page and look for links inside it, then according to the provided deapth, it will request a get request to each found link in the target domain and then do the same for the body of the responses.. and so on

`           *******************
Welcome to *** ScraperLoya *** the customizable WebScraber
           *******************
# Welcome to ScraperLoya by Ali.W.Hassan. Please use it only for ethical purposes
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
    -headers        headers to be added (except user-agent) - in dictionarry form: {header1:value,header2:value,header3:value...}`

USAGE:     `python ScraperLoya.py -url [URL] -domain [Domain] -depth [depth] -timeout [timeout] -user-agent [user-agent] -proxy [proxy] -headers [headers]`      (python3)
example:   `python ScraperLoya.py -url http://n1.example.test/ -domain example.test -depth 3 -timeout 30 -user-agent userAgent-file.txt -proxy proxies-file.txt -headers {header1:value1,header2:value2,header3:value3}`
