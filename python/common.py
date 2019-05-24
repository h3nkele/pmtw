
from functools import reduce
import smtplib, ssl

class counter:
    start = 0
    value = 0
    increment = 1

    def __init__(self, start, increment):
        self.start = start
        self.value=start
        self.increment = increment


    def incr(self):
        self.value=self.value+self.increment
        return self.value - 1
class Day:
    weekday = None
    date = None

    def __init__(self, weekday, date):
        self.weekday = weekday
        self.date = date

    def __repr__(self):
        return self.weekday+" ("+self.date+")"

class DayMenu:
    date = None
    menu = None
    
    def __init__(self, date, menu):
        self.date = date
        self.menu = menu
    
    def is_in_menu(self, keywords, comparator_fn):
        comparator_fn = (lambda s1,s2:  s1 in s2)  if comparator_fn == None else comparator_fn
        return reduce(lambda acc1, meal: acc1 or reduce(
                lambda acc2, keyword: acc2 or comparator_fn(keyword, meal)
               , keywords, False)
            , self.menu, False)
    
    def __repr__(self):
        date = (reduce(lambda d1, d2: d1+" "+d2,self.date))if type(self.date)==list else self.date
        c = counter(1,1)
        menu = (" " +str(c.incr())+ " "+reduce(lambda d1, d2: d1+"\n "+str(c.incr())+" "+d2,self.menu))if type(self.menu)==list else '\n\t'+ self.menu
        return "\nDate: "+ str(date) +'\nMenu:\n'+menu

class FoodSite:
    name = None
    keywords = None
    comparator_fn = None
    menu_url = None 
    menu_list = None
    extract_menu_fn = lambda url: None

    def __init__(self, name, menu_url, keywords,extract_menu_fn):
        self.name = name
        self.menu_url = menu_url
        self.extract_menu_fn = extract_menu_fn
        self.update_menu_list()
        self.keywords = keywords

    def __repr__(self):
        return reduce(lambda a, b : str(a)+"\n"+str(b), self.menu_list)

    def update_menu_list(self):
        self.menu_list = self.extract_menu_fn(url=self.menu_url)

    def get_interesting_entrys(self, keywords, comparator_fn):
        keywords = self.keywords if keywords == None else keywords
        comparator_fn = self.comparator_fn if comparator_fn == None else comparator_fn
        return filter(lambda day_menu: day_menu.is_in_menu(keywords, comparator_fn),self.menu_list)

def simplify_string(string):
    return string.strip().replace(" ","").replace("\t","").replace("\n","").replace("\r","").upper()

def send_emails(smtp_server, port, sender_addr, passwd ,receiver_addrs, body):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_addr, passwd)

        subject = "lecker lecker !"

        for rec in receiver_addrs: 
            
            msg =  'From: <'+sender_addr+'>\nTo: <'+rec+'>'+'\nSubject: '+ subject + '\n\n'+body
            print(msg)
            server.sendmail(sender_addr, rec, msg.encode('utf-8'))



