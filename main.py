import requests, os, argparse, colorama, shodan, socket, urllib.request
from colorama import Fore

SHODAN_API_KEY = 'SHODAN API KEY HERE'
api = shodan.Shodan(SHODAN_API_KEY)

parser = argparse.ArgumentParser(description='BHU Web Crawler')
parser.add_argument('-u', '--url', metavar='URL', required=True, help='Website URL')
parser.add_argument('-w', '--wordlist', metavar='PATH', help='Subdomain/Directory Brute Force Wordlist Path | Enables Brute Force')
parser.add_argument('-pa', '--print-all', action='store_true', help='Print Valid and Invalid Subdomains/Directorys')
parser.add_argument('-v', '--verbosity', action='store_true', help='Enable Verbosity')
parser.add_argument('-s', '--shodan', action='store_true', help='Run Shodan Search')
parser.add_argument('-ip', action='store_true', help='Get Websites IP')
parser.add_argument('-o', '--output', metavar='FILENAME', help='Output File')
args = parser.parse_args()

wdl = args.wordlist

if args.output:
	print(f'\n[{Fore.BLUE}+{Fore.RESET}] Directory Results will be Written to {args.output}')
	
	outcl = open(f'{args.output}', 'w')
	outcl.write('')
	outcl.close()

if args.url[-1] == '/':
	urll = args.url[:-1]
else:
	urll = args.url

if 'https://' in urll:
	url = urll.replace('https://', '')
else:
	if 'http://' in urll:
		url = urll.replace('http://', '')
	else:
		url = urll

re = requests.get('https://' + url + '/')

if args.verbosity:
	if re.status_code == 200:
		print(f'\n[{Fore.GREEN}*{Fore.RESET}] {url} is Online | Status Code: {re.status_code}')
	else:
		print(f'\n[{Fore.RED}-{Fore.RESET}] {url} is Offline | Status Code: {re.status_code}')
		print(f'[{Fore.BLUE}*{Fore.RESET}] Maybe Check your Internet Connection...')
		exit()
else:
	if re.status_code == 200:
		print(f'\n[{Fore.GREEN}*{Fore.RESET}] {url} is Online')
	else:
		print(f'\n[{Fore.RED}-{Fore.RESET}] {url} is Offline')
		print(f'[{Fore.BLUE}*{Fore.RESET}] Maybe Check your Internet Connection...')
		exit()
		
if args.shodan:
	print(f'\n[{Fore.YELLOW}*{Fore.RESET}] Performing a Shodan Search')
	
	ffe = open("shodan.txt", 'w')

	try:
		results = api.search(url)
		ffe.write('Results found: {}\n'.format(results['total']))
		for result in results['matches']:
			ffe.write('IP: {}'.format(result['ip_str']))
			ffe.write(result['data'])
		print(f'\n[{Fore.GREEN}+{Fore.RESET}] Wrote Shodan Data in shodan.txt')
		ffe.close()
	except:
		print(f'\n[{Fore.RED}-{Fore.RESET}] Shodan API Error')
		ffe.close()

if args.ip:
	print(f'\n[{Fore.GREEN}+{Fore.RESET}] Website IP: {socket.gethostbyname(url.replace("https://", ""))}')

if args.wordlist:
	req = requests.get('https://' + url + '/robots.txt')
	if req.status_code == 200:
		if args.verbosity:
			print(f'\n[{Fore.GREEN}+{Fore.RESET}] robots.txt Found > https://{url}/robots.txt | Status Code {req.status_code}')
		else:
			print(f'\n[{Fore.GREEN}+{Fore.RESET}] robots.txt Found > https://{url}/robots.txt')
	else:
		if args.verbosity:
			print(f'\n[{Fore.RED}-{Fore.RESET}] No robots.txt Found | Status Code {req.status_code}')
		else:
			print(f'\n[{Fore.RED}-{Fore.RESET}] No robots.txt Found')
			
if args.wordlist:
	with open(f'{wdl}', 'r') as fp:
		for count, line in enumerate(fp):
			pass
			
	print(f'\n[{Fore.YELLOW}*{Fore.RESET}] Wordlist Length > {count + 1}\n')
	
	print(f'[{Fore.MAGENTA}*{Fore.RESET}] If This Attack Fails Try www.{url}\n')

	while True:
		printline = 1
		lineCounter = 0
		with open(f'{wdl}', 'r') as f:
			for line in f:
				lineCounter += 1
				if lineCounter == printline:
					if printline == count:
						exit()
					if args.output:
						foutbf = open(f'{args.output}', 'a')
					linel = line.replace('''
''', '')
					try:
						r = urllib.request.urlopen('https://' + url + '/' + linel).getcode()
						if r == 200:
							if args.verbosity:
								print(f'[{Fore.GREEN}+{Fore.RESET}] \033[1m{linel}\033[0m is Valid | Status Code \033[1m{r}\033[0m | https://{url}/{linel}')
								if args.output:
									foutbf.write(f'[+] {linel} is Valid | Status Code {r} | https://{url}/{linel}\n')
							else:
								print(f'[{Fore.GREEN}+{Fore.RESET}] \033[1m{linel}\033[0m is Valid | https://{url}/{linel}')
								if args.output:
									foutbf.write(f'[+] {linel} is Valid | https://{url}/{linel}\n')
					except:
						if args.print_all:
								if args.verbosity:
									print(f'[{Fore.RED}-{Fore.RESET}] \033[1m{linel}\033[0m is Invalid | Status Code \033[1m{r}\033[0m | https://{url}/{linel}')
									if args.output:
										foutbf.write(f'[-] {linel} is Invalid | Status Code {r} | https://{url}/{linel}\n')
								else:
									print(f'[{Fore.RED}-{Fore.RESET}] \033[1m{linel}\033[0m is Invalid | https://{url}/{linel}')
									if args.output:
										foutbf.write(f'[-] {linel} is Invalid | https://{url}/{linel}\n')
						else:
							pass
					printline += 1
