import psycopg2


class Postgers:
    def __init__(self):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = psycopg2.connect(database="d8e59igo676alv", user="dnwcmkwujqwacd",
            password="55c82317567631a79b54d3db7fdd758a152f9542f2fb98408c6128927dd9551a",
            host="ec2-107-22-241-205.compute-1.amazonaws.com", port=5432)
        self.cursor = self.connection.cursor()

    def insert(self, long_url, short_url, token):
        """Записываем в бд"""
        self.cursor.execute('''INSERT INTO main (long_url, short_url, token)
                               VALUES ('{0}', '{1}', '{2}')'''.format(long_url, short_url, token))
        self.connection.commit()

    def is_unic(self, token):
        """Проверяем токен на уникаальность"""
        self.cursor.execute('''SELECT id FROM main WHERE token = '{}' '''.format(token))
        if len(self.cursor.fetchall()) > 1:
            return False
        else:
            return True

    def select(self, token):
        """Получаем полную ссылку"""
        self.cursor.execute('''SELECT long_url FROM main WHERE token = '{}' '''.format(token))
        return self.cursor.fetchall()[0][0]

    def count_plus(self, token):
        """Счетчик переходов по ссылке"""
        self.cursor.execute('''SELECT count FROM main WHERE token = '{}' '''.format(token))
        count = self.cursor.fetchall()[0][0]
        if count == None:
            count = 1
        else:
            count += 1
        self.cursor.execute('''UPDATE main
                               SET count = {0}
                               WHERE token = '{1}' '''.format(count, token))
        self.connection.commit()

    def select_count(self, token):
        """Смотри сколько было переходов по ссылке"""
        self.cursor.execute('''SELECT count FROM main WHERE token = '{}' '''.format(token))
        return self.cursor.fetchall()[0][0]


    def delete(self, token):
        self.cursor.execute('''DELETE * FROM main WHERE token = '{}' '''.format(token))
        self.connection.commit()


db = Postgers()
# print(dbs.is_unic('271d'))
# db.insert('https://habr.com/ru/company/skillbox/blog/464705/', 'http://127.0.0.1:5000/d-sh/271f93', '271f93')
# print(db.count_plus('271f93'))
# print(db.select_count('271f93'))
# print(db.select('http://127.0.0.1:5000/d-sh/abd375'))
