import socket
import os
import sys
import requests
import folium as fo
import re
from pyfiglet import Figlet
from clint.textui import colored
from clint.textui import puts, indent


COMMANDS = ['help', '?', 'exit', 'ping', 'whois', 'geoip', 'iptoasn', 'asntoip', 'dns', 'settings', 'reload']


def onstart():
    if os.name == "nt":
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    else:
        pass

    f = Figlet(font='puffy')
    with indent(15):
        puts(colored.cyan(f.renderText('Wack 1.0')))

    with indent(35):
        puts(colored.white('Redesigned.'))

    with indent(30):
        puts(colored.white('Created by: ') + colored.blue('JXRIS'))

    with indent(30):
        localip = socket.gethostbyname(socket.gethostname())
        puts(colored.white(f'\nYour IP: {colored.blue(localip)}'))

    with indent(34):
        puts(colored.white(f'Your OS: {colored.blue(sys.platform)}'))

    with indent(20):
        puts(colored.white('\n\n\nTry "help" to see which commands are avaible.'))
    commandhandler()


def help():
    print(colored.green('[+] exit - Quits the application.'))
    print(colored.green('[+] ping - Pings an IP address.'))
    print(colored.green('[+] whois - Gets the WHOIS information from a domain.'))
    print(colored.green('[+] geoip - Gets the latitude and longitude of an IP.'))
    print(colored.green('[+] iptoasn - Gets ASN from IP.'))
    print(colored.green('[+] asntoip - Gets IP from ASN.'))
    print(colored.green('[+] dns - Gets DNS info from domain.'))


def pinger():
    ip = input(colored.green('[+] Please enter an IP: '))
    try:
        response = requests.get(f'https://api.hackertarget.com/nping/?q={ip}')
        print(colored.yellow(f'[+] Now starting to ping {ip}...'))
        if response.status_code == 200:
            print(colored.green(response.text))
        else:
            print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))
    except:
        print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))


def whoiscmd():
    domain = input(colored.green('[+] Please enter a domain name: '))
    print(colored.yellow(f'[+] Looking up WHOIS info for {domain}'))
    try:
        response = requests.get(f'https://api.hackertarget.com/whois/?q={domain}')
        if response.status_code == 200:
            print(colored.green(response.text))
        else:
            print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))
    except:
        print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))


def iptogeo():
    ip = input(colored.green('[+] Please enter an IP: '))
    try:
        print(colored.yellow(f'[+] Looking up GEOIP info for {ip}'))
        response = requests.get(f'https://api.hackertarget.com/geoip/?q={ip}')
        if response.status_code == 200:
            print(colored.green(response.text))
            q = input(colored.green('\nWould u like to view it on a map? y/n:\n'))


            if q == 'y':
                converted = response.text.split('Latitude')[1]
                coords = re.findall('\d+', converted)
                c0 = coords[0]
                c1 = coords[1]
                c2 = coords[2]
                c3 = coords[3]
                final1 = c0 + '.' + c1
                final2 = c2 + '.' + c3
                x = fo.FeatureGroup(name='Target')
                loc = [final1, final2]
                x.add_child(fo.Marker(location=loc, popup=f'Target found at {final1},{final2}', icon=fo.Icon(color='green')))
                m = fo.Map()
                m.add_child(x)
                m.save('map.html')
                print(colored.green('[+] Map created. Saved in current work directory.'))
            elif q == 'n':
                pass
            else:
                print(colored.red('[+] I did not recognize that input. Select "y" or "n".'))

        else:
            print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))
    except:
        print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))


def iptoasn():
    ip = input(colored.green('[+] Please enter an IP: '))
    try:
        print(colored.yellow(f'[+] Looking up ASN info for {ip}.'))
        response = requests.get(f'https://api.hackertarget.com/aslookup/?q={ip}')
        if response.status_code == 200:
            print(colored.green(response.text))
        else:
            print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))
    except:
        print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))


def asntoip():
    asn = input(colored.green('[+] Enter the ASN: '))
    try:
        print(colored.yellow(f'[+] Looking up ASN info for {asn}.'))
        response = requests.get(f'https://api.hackertarget.com/aslookup/?q={asn}')
        if response.status_code == 200:
            print(colored.green(response.text))
        else:
            print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))
    except:
        print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))


def dns():
    domain = input(colored.green('[+] Please enter a domain name: '))
    print(colored.yellow(f'[+] Looking up DNS info for {domain}'))
    try:
        response = requests.get(f'https://api.hackertarget.com/dnslookup/?q={domain}')
        if response.status_code == 200:
            print(colored.green(response.text))
        else:
            print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))
    except:
        print(colored.red('[+] Looks like something went wrong, please check your internet connection.'))



def commandhandler():
    cmd = input(colored.green('\n\n\nwack@root $ '))

    while cmd not in COMMANDS:
        print(colored.red('[+] Unknown command. Try "help" to see which commands are avaible, type "exit" to leave.'))
        cmd = input(colored.green('\n\nwack@root $ '))


    if cmd == "exit":
        exit()
    elif cmd == "help":
        help()
    elif cmd == "ping":
        pinger()
    elif cmd == "whois":
        whoiscmd()
    elif cmd == "geoip":
        iptogeo()
    elif cmd == 'iptoasn':
        iptoasn()
    elif cmd == 'asntoip':
        asntoip()
    elif cmd == 'dns':
        dns()
onstart()

while True:
    commandhandler()
