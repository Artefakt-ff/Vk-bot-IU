from json import load
from datetime import date, time, datetime
from components.settings import days_in_week, lessons_time


def get_day(offset):  # ask for schedule of current day, return dict
    with open('schedule.txt', encoding='utf-8', errors='ignore') as f:
        return load(f)[days_in_week[(date.today()).weekday()+offset]]


def get_number_of_lesson():  # возвращает текущий урок
        now = time(datetime.now().hour, datetime.now().minute)
        number_of_lesson = None
        for i in range(len(lessons_time)):  # compare time of lesson and actual time, find number of lesson
            if lessons_time[i][0] < now < lessons_time[i][1]:
                number_of_lesson = i  # if we have a lesson then return number of it
                break
            else:
                try:
                    if lessons_time[i][1] < now < lessons_time[i+1][0]:  # if time between lessons then it is break
                        number_of_lesson = ('break', i)  # if we have a break then return a tupple
                        break
                except IndexError:
                    pass
        return number_of_lesson  # Return number in order of lesson


class Now:
    def __init__(self):
        self.beautiful_output = ''
        self.schedule = get_day(0)
        self.number_of_lesson = get_number_of_lesson()
        self.number_of_week = ((datetime.today() - datetime(2017, 9, 1)).days+1) // 7
        if (((datetime.today() - datetime(2017, 9, 1)).days // 7 + 1) % 2) == 1:
            self.state_of_week = 'числитель'
            self.lessons = self.schedule['NUM']
            self.rooms = self.schedule['NUM_ROOM']
        else:
            self.state_of_week = 'знаменатель'
            self.lessons = self.schedule['DEN']
            self.rooms = self.schedule['DEN_ROOM']
        if self.number_of_lesson is None:
            """ Вот это все веселье значит:
            1) Если сейчас не перемена и не урока - этот и следущий урок - None
            2) Если сейчас перемена то приходит кортеж с первым элементом "break" и во вторым номером только
            что закончившегося урока. Текущий урок - None, следующий урок, если последний тоже.
            3) Если сейчас урок, то пробуем узнать следующий, если нет - None"""
            self.lesson = None
            self.room = None
            self.next_lesson = None
            self.next_room = None

        elif type(self.number_of_lesson) == tuple:
            self.lesson = None
            self.room = None
            try:
                self.next_lesson = self.lessons[self.number_of_lesson[1]]
                self.next_room = self.rooms[self.number_of_lesson[1]]
            except IndexError:
                self.next_lesson = None
                self.next_room = None
            self.number_of_lesson = self.number_of_lesson[0]
        else:
            self.lesson = self.lessons[self.number_of_lesson]
            self.room = self.lessons[self.number_of_lesson]
            try:
                self.next_lesson = self.lessons[self.number_of_lesson+1]
                self.next_room = self.rooms[self.number_of_lesson+1]
            except IndexError:
                self.next_lesson = None
                self.next_room = None
        for i in range(len(self.lessons)):
            if self.lessons[i] is not None:
                self.beautiful_output += str(i) + ' ' + self.lessons[i] + '\n'


class Tomorrow:
    def __init__(self):
        offset = 1
        try:  # if it's Sunday
            get_day(1)
        except KeyError:
            offset = -6
        self.schedule = get_day(offset)
        self.beautiful_output = ''
        self.number_of_week = (datetime.today() - datetime(2017, 9, 1)).days // 7 + 1
        if (((datetime.today() - datetime(2017, 9, 1)).days // 7 + 1) % 2) == 1:
            self.state_of_week = 'числитель'
            self.lessons = self.schedule['NUM']
            self.rooms = self.schedule['NUM_ROOM']
        else:
            self.state_of_week = 'знаменатель'
            self.lessons = self.schedule['DEN']
            self.rooms = self.schedule['DEN_ROOM']
        for i in range(len(self.lessons)):
            if self.lessons[i] is not None:
                self.beautiful_output += str(i) + ' ' + self.lessons[i] + '\n'

