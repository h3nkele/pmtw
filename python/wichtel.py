import requests_html as html
from common import Day, DayMenu

url = 'https://www.wichtel.de/locations/boeblingen/weekly-menu/aktuelle-wochenkarte/'

    
def gen_week_menu_wichtel(url):
    tr_iter =iter(html.HTMLSession()
        .get(url)
        .html.find('.menu-of-week', first = True)
        .find('tr')[1:])
    menu = []
    while (True):
        try:
            item = next(tr_iter)
            if (item.find('.day-of-week', first=True) != None):
                tmp = item.find('td')
                day = Day(tmp[0].text, tmp[1].text)
                menu.append(DayMenu(day, []))
            elif (item.find('td', containing="Suppe", first=True) != None
            or item.find('td', containing="Essen", first=True) != None
            or item.find('td', containing="Dessert", first=True) != None):
                menu[-1].menu.append(item.find('td')[1].text)
        except StopIteration:
            break
    return menu