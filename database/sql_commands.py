import sqlite3

from database import sql_queries


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")
        self.cursor = self.connection.cursor()

    def sql_create_user_table_query(self):
        if self.connection:
            print("Database connected successfully")
        self.connection.execute(sql_queries.create_user_table_query)
        self.connection.execute(sql_queries.create_quiz)
        self.connection.execute(sql_queries.create_user_ban)
        self.connection.execute(sql_queries.create_user_survey)
        self.connection.execute(sql_queries.create_complaint)

    def sql_insert_user_table_query(self, telegram_id, username, first_name, last_name):
        self.cursor.execute(sql_queries.insert_user_table_query, (telegram_id,
                                                                  username,
                                                                  first_name,
                                                                  last_name,))
        self.connection.commit()

    def sql_select_user_table_query(self):
        self.cursor.row_factory = lambda cursor, row: {"telegram_id": row[1],
                                                       "username": row[2],
                                                       "first_name": row[3],
                                                       "last_name": row[4]}
        return self.cursor.execute(sql_queries.select_user_table_query).fetchall()

    def sql_insert_quiz(self, telegram_id, quiz, quiz_option):
        self.cursor.execute(sql_queries.insert_quiz, (telegram_id,
                                                      quiz,
                                                      quiz_option,))
        self.connection.commit()

    def sql_insert_user_ban(self, telegram_id, group_id, reasons):
        self.cursor.execute(sql_queries.insert_user_ban, (telegram_id,
                                                          group_id,
                                                          reasons,))
        self.connection.commit()

    def sql_select_user_ban(self, telegram_id, group_id):
        self.cursor.row_factory = lambda cursor, row: {"telegram_id": row[0]}
        return self.cursor.execute(sql_queries.select_user_ban, (telegram_id,
                                                                 group_id)).fetchall()

    def sql_select_potential_user_ban(self):
        self.cursor.row_factory = lambda cursor, row: {"telegram_id": row[1],
                                                       "username": row[2],
                                                       "first_name": row[3],
                                                       "last_name": row[4],
                                                       "reasons": row[9]}
        return self.cursor.execute(sql_queries.select_potential_user_ban).fetchall()

    def sql_insert_user_survey(self, idea, problems, assessment, user_id):
        self.cursor.execute(sql_queries.insert_user_survey, (idea,
                                                             problems,
                                                             assessment,
                                                             user_id,))
        self.connection.commit()

    def sql_select_user_survey(self):
        self.cursor.row_factory = lambda cursor, row: {"id": row[0],
                                                       "idea": row[1],
                                                       "problems": row[2],
                                                       "assessment": row[3],
                                                       "user_id": row[4]}
        return self.cursor.execute(sql_queries.select_user_survey).fetchall()

    def sql_select_user_survey_by_id(self, id):
        self.cursor.row_factory = lambda cursor, row: {"id": row[0],
                                                       "telegram_id": row[1],
                                                       "username": row[2],
                                                       "first_name": row[3],
                                                       "last_name": row[4],
                                                       "idea": row[6],
                                                       "problems": row[7],
                                                       "assessment": row[8]}
        return self.cursor.execute(sql_queries.select_user_survey_by_id, (id,)).fetchall()

    def sql_insert_complaint(self, telegram_id, telegram_id_bad_user, reason, count):
        self.cursor.execute(sql_queries.insert_complaint, (telegram_id,
                                                           telegram_id_bad_user,
                                                           reason,
                                                           count,))
        self.connection.commit()

    def sql_select_id_by_username(self, username):
        self.cursor.row_factory = lambda cursor, row: {"username": row[0]}
        return self.cursor.execute(sql_queries.select_id_by_username, (username,)).fetchall()

    def sql_select_complaint(self, user_id):
        self.cursor.row_factory = lambda cursor, row: {"count": row[0]}
        return self.cursor.execute(sql_queries.select_complaint, (user_id,))

    def sql_select_complaint_check(self, user_id, bad_user_id):
        self.cursor.row_factory = lambda cursor, row: {"count": row[0]}
        return self.cursor.execute(sql_queries.select_complaint_check, (user_id, bad_user_id,))
