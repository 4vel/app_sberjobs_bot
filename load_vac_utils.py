import logging
from dbsrc import DataAccessLayer, Vacancy
from data.config import conn_string
from parser import VacancyParser
from sqlalchemy.exc import DBAPIError



def clean_table(dal):
    try:
        dal.connect()
        num_rows_deleted = dal.session.query(Vacancy).delete()
        logging.info(f'Удаляю данные Vacancy. Удалено {num_rows_deleted}')
        dal.session.commit()
    except DBAPIError as exc:
        logging.info(f'{exc}')
        dal.session.rollback()


def parse_vacancies():
    vp = VacancyParser()
    vp.get_vacancies()
    vp.show_info()
    vacancy_objects = vp.get_list_of_vacancies_obj()
    return vacancy_objects


def insert_into_db(dal, vacancy_objects):
    try:
        dal.connect()
        logging.info("Сохраняю вакансии в БД")
        dal.session.bulk_save_objects(vacancy_objects)
        dal.session.commit()

    except DBAPIError as exc:
        logging.info(f'{exc}')
        dal.session.rollback()


def load_vacancies_pipeline():
    print("Начинаю пайплайн")
    dal = DataAccessLayer(conn_string)

    clean_table(dal)
    vacancy_objects = parse_vacancies()
    insert_into_db(dal, vacancy_objects)

def healthcheck():
    print("💟")