import logging
from dbsrc import Vacancy
from sqlalchemy.exc import SQLAlchemyError


def get_num_vacancies(session):
    session = session()
    rows = session.query(Vacancy).count()
    session.commit()
    return rows


def get_num_vacancies_by_key_words(session):
    session = session()
    list_of_vacs = session.query(Vacancy.vacid).filter(Vacancy.vactitle.op('~')(r"python|Руководитель")).all()
    session.commit()

    return len(list_of_vacs)


def get_vacancies(session):
    session = session()
    list_of_vacs = session.query(Vacancy.vacid).all()
    session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]
    return list_of_vacs


def get_first_vacancy_id(session):
    session = session()
    list_of_vacs = session.query(Vacancy.vacid).first()
    session.commit()
    vacancy_id = list_of_vacs[0]

    return vacancy_id


def get_vacancies_by_key_words(session):
    session = session()
    list_of_vacs = session.query(Vacancy.vacid).filter(Vacancy.vactitle.op('~')(r"python|Руководитель")).all()
    session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]

    return list_of_vacs


def get_vacancy_obj(vac_id, session):
    session = session()
    vobj = session.query(Vacancy).filter(Vacancy.vacid == vac_id).first()
    session.commit()
    return vobj


def previous_current_next(iterable):
    """Создает итератор который выдает таплы (предыдущий, текущий, следующий)

    Если нет значения, то значения предыдущего или следующего, то возвращает None

    """
    iterable = iter(iterable)
    prv = None
    cur = next(iterable)
    try:
        while True:
            nxt = next(iterable)
            yield prv, cur, nxt
            prv = cur
            cur = nxt
    except StopIteration:
        yield prv, cur, None


def add_user_to_db(record, session):
    """ Добавляем пользователя в базу данных """
    try:
        session = session()
        session.add(record)
        session.commit()
        logging.info("Данные пользователя добавлены")
    except SQLAlchemyError as err:
        logging.info(err)


def update_user_data_in_db():
    pass


def delete_user_in_db():
    pass
