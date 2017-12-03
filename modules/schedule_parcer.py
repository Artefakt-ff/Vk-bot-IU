from urllib import request
from bs4 import BeautifulSoup
from json import dumps

ids = {'ИУ3-12Б': '40545dd8-c780-11e6-87a5-005056960017'}


def get_actual_lesson(group):
    """Return the dictionary with actual time-table. Usage: dic[day][key]. Day is in russian, starts full word with capital letter
    Possible keys: TIME, NUM, DEN, NUM_ROOM, DEN_ROOM."""
    db = {}
    url = 'https://students.bmstu.ru/schedule/' + ids[group]  # Read the site
    with request.urlopen(url) as req:
        site = req.read()

    site = BeautifulSoup(site, "lxml")  # New object "Soup"

    tables = site.find_all('div', class_='col-md-6 hidden-sm hidden-md hidden-lg')  # Find all days

    for table in tables:  # Explore all days
        tds = table.find_all('td')
        day = tds[0].string
        db[day] = {'TIME': [], 'NUM': [], 'DEN': [], 'NUM_ROOM': [], 'DEN_ROOM': []}
        db['Воскресение'] = {'TIME': ['08:30 - 10:05', '10:15 - 11:50', '12:00 - 13:35', '13:50 - 15:25', '15:40 - 17:15',
                             '17:25 - 19:00', '19:10 - 20:45'], 'NUM_ROOM': [None, None, None, None, None, None, None],
                             'DEN_ROOM': [None, None, None, None, None, None, None],
                             'DEN': [None, None, None, None, None, None, None],
                             'NUM': [None, None, None, None, None, None, None]}

        count = 3
        for j in range(7):
            count += 1
            db[day]['TIME'].append(tds[count].string)
            count += 1
            if 'colspan' in str(tds[count]):  # If lesson take and numerator, and denominator
                db[day]['NUM'].append(tds[count].span.string)
                db[day]['DEN'].append(tds[count].span.string)
                db[day]['NUM_ROOM'].append(tds[count].i.string)
                db[day]['DEN_ROOM'].append(tds[count].i.string)
            else:
                try:  # If only in denominator or in numerator
                    db[day]['NUM'].append(tds[count].span.string)
                    db[day]['NUM_ROOM'].append(tds[count].i.string)
                    count += 1
                    db[day]['DEN'].append(tds[count].span.string)
                    db[day]['DEN_ROOM'].append(tds[count].i.string)
                except AttributeError:  # If no lesson
                    db[day]['NUM_ROOM'].append(None)
                    db[day]['NUM'].append(None)
                    count += 1
                    db[day]['DEN_ROOM'].append(None)
                    db[day]['DEN'].append(None)

    return db

schedule = get_actual_lesson('ИУ3-12Б')

with open('../schedule.txt', 'w', encoding='utf-8') as f:
    f.write(dumps(schedule, indent=4,  ensure_ascii=False))
