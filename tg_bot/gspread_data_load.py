import logging

import gspread
from gspread import SpreadsheetNotFound

from google.oauth2.service_account import Credentials

from web_panel.models  import Region, City, Firm, UserProfile

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    r'C:\Users\Aleksandr\AppData\Roaming\gspread\service_account.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)


def check_gspread_connetctions():
    pass


QUESTION_TABLE_NAME = "Профсоюз.Телегрaм.Вопросы"
FIRM_TABLE_NAME = "Профсоюз.Телегрaм.Предприятия"
USERS_TABLES = "Профсоюз.Телегрaм.Пользователи."

ADMIN_EMAIL = " bambruysk@gmail.com"

def get_or_create_spreadsheet(name):
    try:
        sh = gc.open(name)
    except SpreadsheetNotFound:
        sh = gc.create(name)
    # sh.share(ADMIN_EMAIL, perm_type='user', role='owner')
    return sh

def get_spreadsheet(name : str) -> gspread.Spreadsheet:
    try:
        sh = gc.open(name)
    except SpreadsheetNotFound:
        logging.critical(f"Spread sheet {name} not founs")
        raise SpreadsheetNotFound
    return sh


def load_regions():
    sh = get_or_create_spreadsheet(FIRM_TABLE_NAME)
    try:
        regions = sh.worksheet("Области")
    except KeyError:
        logging.log(logging.CRITICAL, "Не найдена таблица областей")
        return
    for r in regions.get_all_records():
        reg, cr = Region.get_or_create(name=r["Область"], head_user_id=1)
        reg.save()


def load_cities():
    sh = get_or_create_spreadsheet(FIRM_TABLE_NAME)
    try:
        cities = sh.worksheet("Города")
    except KeyError:
        logging.log(logging.CRITICAL, "Не найдена таблица городов")
        return
    for r in cities.get_all_records():
        reg, cr = City.get_or_create(
            name=r["Город"],
            head_user_id=1)
        reg.save()


def load_firms():
    sh = get_or_create_spreadsheet(FIRM_TABLE_NAME)
    try:
        firms = sh.worksheet("Фирмы")
    except KeyError:
        logging.log(logging.CRITICAL, "Не найдена таблица городов")
        return
    created_counter = 0
    for r in firms.get_all_records():
        city_name = r.get("Город")
        if not city_name:
            logging.log(logging.CRITICAL, f"Город не указан")
            raise KeyError
        try:
            city = City.objects.get(name=city_name)
        except:
            logging.log(logging.CRITICAL, f"Город {city_name}  не найден.")
            return
        reg, cr = Firm.objects.et_or_create(
            name=r["Фирма"],
            head_user_id=1,
            city=city
        )
        if cr :
            pass
        created_counter += 1
        reg.save()
    logging.info(f"Загружена инофрмация о {created_counter} фирмах")


def load_users(firm_name: str):
    sh = get_or_create_spreadsheet(USERS_TABLES + firm_name)
    try:
        firm = Firm.objects.get(name=firm_name)
    except Firm.DoesNotExist:
        logging.log(logging.CRITICAL, "Фмрма не найдена в базе данных")
        return ()
    users_recs = sh.sheet1.get_all_records()
    for u in users_recs:
        user, cr = UserProfile.objects.get_or_create(
            work_place=firm,
            first_name=u["Имя"],
            last_name=u["Фамилия"],
            father_name=u["Отчество"],
            department=u["Отдел"],
            position=u["Должность"],
            ticket_id=u["Номер билета"]
        )
        user.save()



load_regions()
load_cities()
load_firms()
load_users("РПКБ")




def make_question(firm: str):
    pass


def load_questions():
    sh = gc.open(QUESTION_TABLE_NAME)
    qtable = sh.sheet1.get_all_records()
    qtables = sh.worksheets()

    for qtable in qtables:
        print(qtable.get_all_records())
    pass


def make_root_question(firm_list):
    pass


load_questions()
