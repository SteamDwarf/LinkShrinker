from xml.etree.ElementTree import TreeBuilder
from mysql.connector import connect, Error

connection = None


def init_db():
    global connection
    try:
        print('Подключение к БД:', end='')
        connection = connect(host='db', user='root', password='123')
        print('ОК')

        print('Создание БД:', end='')
        create_db_query = "CREATE DATABASE IF NOT EXISTS links"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
        print('ОК')

        print('Изменение ДБ:', end='')
        use_db_query = "USE links"
        with connection.cursor() as cursor:
            cursor.execute(use_db_query)
        print('ОК')

        print('Создание таблицы:', end='')
        create_table_query = """
        CREATE TABLE IF NOT EXISTS links(
            token VARCHAR(100) PRIMARY KEY,
            password VARCHAR(100),
            source_link VARCHAR(1000),
            UNIQUE (token)
            )
            """
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
        print('ОК')

        print('Описание созданной таблицы:')
        created_table_information = """
        DESCRIBE links;
        """
        with connection.cursor() as cursor:
            cursor.execute(created_table_information)
            for var in cursor:
                print(var)
        print('\n')

    except Error as e:
        print('Fail', e)

def get_link_information(token):
    select_query = f"""
    SELECT * FROM links
    WHERE token = '{token}'
    """

    with connection.cursor(dictionary = True) as cursor:
        cursor.execute(select_query)
        return cursor.fetchone()


def set_link(token, password, source_link):
    insert_query = f"""
    INSERT INTO links (token, password, source_link)
    VALUES (%s,%s,%s)
    """

    with connection.cursor(dictionary = True) as cursor:
        cursor.execute(insert_query, (token, password, source_link))
        connection.commit()


