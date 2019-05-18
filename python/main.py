#!/usr/bin/python

import requests_html as html
from functools import reduce
import smtplib, ssl
import argparse

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
            server.sendmail(sender_addr, rec, msg)

def get_week_menu(address):
    html_content = html.HTMLSession().get(address)
    table_iter = iter(html_content.html.find('.menu-of-week', first = True).find('tr')[1:])
    return gen_week_menu(table_iter)

def gen_week_menu(tr_iter):
    menu = []
    while (True):
        try:
            item = next(tr_iter)
            
            if (item.find('.day-of-week', first=True) != None):
                menu.append(DayMenu(item.find('td')[0].text, [], []))
            elif (item.find('td', containing="Suppe", first=True) != None):
                menu[-1].soups.append(item.find('td')[1].text)
                #print(menu[-1].soups[-1])
            elif (item.find('td', containing="Essen", first=True) != None):
                menu[-1].meals.append(item.find('td')[1].text)
        except StopIteration:
            break
    return menu


def simplify_string(string):
      return string.strip().replace(" ","").replace("\t","").replace("\n","").replace("\r","").upper() 



def main():
    parser = argparse.ArgumentParser(description="Which 'wichtel' url should be seached for which keywords?")
    parser.add_argument('-u','--url', required=True, metavar='URL', type=str, help="The url to the weekly 'wichtel' menu")
    parser.add_argument('-l', '--link', metavar='host', type=str, help='Smtp server', default='smtp.gmail.com')
    parser.add_argument('-p', '--port', metavar='port', type=int, help="The port for the smtp server", default=465)
    parser.add_argument('-e', '--email',required=True, metavar='email', type=str, help='Email address of the sender')
    parser.add_argument('-c', '--code',required=True, metavar='password', type=str, help='Password of sender email')
    parser.add_argument('-s', '--soups', metavar='soup', nargs='*' , type=str, help='Keywords to check in soups menu')
    parser.add_argument('-m', '--meals', metavar='meal', nargs='*' , type=str, help='Keywords to check in meals menu')
    parser.add_argument('-r', '--recipients', metavar='email', nargs='*' , type=str, help='Email addresses of people to notify')
    
    args = parser.parse_args()
    week_menu = get_week_menu(args.url)

    #get_week_menu('https://www.wichtel.de/locations/boeblingen/weekly-menu/aktuelle-wochenkarte/')
    
    
    #print(map(lambda trigger: trigger.upper(), args.soups))
    soup_match = []
    meal_match = []
    if (args.soups != None):
        soup_match = list(
        filter(
            lambda wd : reduce(
                lambda k,l: k or l
                , map(
                    lambda s: reduce(
                        lambda o, n : o or n
                        , map(
                            lambda tr: simplify_string(tr)
                                    in simplify_string(s),
                            args.soups
                        )
                    ) 
                ,wd.soups
                )
            )
            if len(wd.soups)>0 else False
            , week_menu
        )
        )
        

    if (args.meals != None):
        meal_match = list(
        filter(
            lambda wd : reduce(
                lambda k,l: k or l
                , map(
                    lambda m: reduce(
                        lambda o, n : o or n
                        , map(
                            lambda tr: simplify_string(tr)
                                    in simplify_string(m),
                            args.meals
                        )
                    ) 
                ,wd.meals
                )
            )
            if len(wd.meals)>0 else False
            ,week_menu
        )
        )
    
    mail_text=""

    soup_bool = len(soup_match) > 0
    meal_bool = len(meal_match) > 0

    if (soup_bool):
        mail_text+="Interessantes bei Suppen:\n\t"+str(reduce(lambda a,b:str(a)+'\n\t'+str(b)if b != None else "", soup_match))+'\n'
    if (meal_bool):
        mail_text+="Interessantes bei Gerichten:\n\t"+str(reduce(lambda a,b:str(a)+'\n\t'+str(b)if b != None else "", meal_match))+'\n'  
    #print(mail_text)
    
    if (soup_bool or meal_bool): send_emails(args.link, args.port, args.email, args.code ,args.recipients, mail_text)



if __name__ == "__main__":
    main()
