#!/usr/bin/python

import requests_html as html
from functools import reduce
import smtplib, ssl
import argparse
import wichtel
import common

import sys


class DayMenu:
    date = ""
    soups = []
    meals = []
    def __init__(self, date, soups, meals):
        self.date=date
        self.soups=soups
        self.meals=meals

    def __repr__(self):
        soups_str = "" if len(self.soups) < 1 else reduce(lambda a, b : a + ", " + b if b != None else "", self.soups)
        meals_str = "" if len(self.meals) < 1 else reduce(lambda a, b : a + ", " + b if b != None else "", self.meals)
        return "day: "+ self.date+", soups: "+ soups_str+", meals: "+meals_str
        
def send_emails(smtp_server, port, sender_addr, passwd ,receiver_addrs, body):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_addr, passwd)

        subject = "lecker lecker !"

        for rec in receiver_addrs: 
            
            msg =  'From: <'+sender_addr+'>\nTo: <'+rec+'>'+'\nSubject: '+ subject + '\n\n'+body
            print(msg)
            server.sendmail(sender_addr, rec, msg.encode('utf-8'))





def main():
    parser = argparse.ArgumentParser(description="Which 'wichtel' url should be seached for which keywords?")
    parser.add_argument('-l', '--link', metavar='host', type=str, help='Smtp server', default='smtp.gmail.com')
    parser.add_argument('-p', '--port', metavar='port', type=int, help="The port for the smtp server", default=465)
    parser.add_argument('-e', '--email',required=True, metavar='email', type=str, help='Email address of the sender')
    parser.add_argument('-c', '--code',required=True, metavar='password', type=str, help='Password of sender email')
    parser.add_argument('-k', '--keywords', metavar='keywords', nargs='*' , type=str, help='Keywords and phrases to check in meals menu')
    parser.add_argument('-r', '--recipients', metavar='email', nargs='*' , type=str, help='Email addresses of people to notify')
    
    args = parser.parse_args()
    
    wichtel_menu = common.FoodSite(name='Wichtel', menu_url=wichtel.url, keywords=args.keywords, extract_menu_fn=wichtel.gen_week_menu_wichtel)
    wichtel_matches = list(wichtel_menu.get_interesting_entrys(keywords=None, comparator_fn=lambda a, b: common.simplify_string(a)in common.simplify_string(b)))

    mail_text = ""
    wichtel_bool = len(wichtel_matches) > 0
    if (wichtel_bool):
        mail_text+="Interessantes beim Wichtel:\n\t"+str(reduce(lambda a,b:str(a)+'\n\t'+str(b)if b != None else "", wichtel_matches))+'\n'

    print(mail_text)
    
    if (wichtel_bool): send_emails(args.link, args.port, args.email, args.code ,args.recipients, mail_text)



if __name__ == "__main__":
    main()
