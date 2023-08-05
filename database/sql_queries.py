create_user_table_query = """
        CREATE TABLE IF NOT EXISTS telegram_users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        telegram_id INTEGER,
        username CHAR(50), 
        first_name CHAR(50), 
        last_name CHAR(50),
        reference_link TEXT NULL,
        UNIQUE (telegram_id))
"""
insert_user_table_query = """
    INSERT OR IGNORE INTO telegram_users (telegram_id, username, first_name, last_name) VALUES (?,?,?,?)
"""
select_user_table_query = """
    SELECT * FROM telegram_users
"""

create_quiz = """
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        quiz CHAR(10),
        quiz_option INTEGER,
        FOREIGN KEY (telegram_id) REFERENCES telegram_users (telegram_id)
    )
"""
insert_quiz = """
    INSERT OR IGNORE INTO quiz (telegram_id, quiz, quiz_option) VALUES (?, ?, ?)
"""

create_user_ban = """
    CREATE TABLE IF NOT EXISTS user_ban (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        group_id INTEGER,
        datetime DATETIME DEFAULT (datetime('now', '+6 hours')) NOT NULL,
        reasons TEXT,
        FOREIGN KEY (telegram_id) REFERENCES telegram_users (telegram_id)
    )
"""
insert_user_ban = """
    INSERT INTO user_ban(telegram_id, group_id, reasons) VALUES (?, ?, ?)
"""
select_user_ban = """
    SELECT telegram_id FROM user_ban WHERE telegram_id == ? AND group_id == ? AND datetime('now', '-18 hours') < datetime('now', '+6 hours')
"""
select_potential_user_ban = """
    SELECT * FROM
        telegram_users
    INNER JOIN
        user_ban
    ON
        telegram_users.telegram_id = user_ban.telegram_id
    WHERE datetime('now', '-18 hours') < datetime('now', '+6 hours')
    GROUP BY telegram_users.telegram_id
    ORDER BY user_ban.datetime DESC;
"""

create_user_survey = """
    CREATE TABLE IF NOT EXISTS user_survey (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idea TEXT,
        problems TEXT,
        assessment INTEGER,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES telegram_users (telegram_id)
    )
"""
insert_user_survey = """
    INSERT INTO user_survey (idea, problems, assessment, user_id) VALUES (?, ?, ?, ?)
"""
select_user_survey = """
    SELECT * FROM user_survey
"""
select_user_survey_by_id = """
    SELECT * FROM
        telegram_users
    LEFT JOIN 
        user_survey
    ON user_survey.user_id = telegram_users.telegram_id
    WHERE user_survey.id = ?
"""

create_complaint = """
    CREATE TABLE IF NOT EXISTS complaint(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        telegram_id_bad_user INTEGER,
        reason TEXT,
        count INTEGER
    )
"""
insert_complaint = """
    INSERT OR IGNORE INTO complaint(telegram_id, telegram_id_bad_user, reason, count)
    VALUES (?, ?, ?, ?)
"""
select_id_by_username = """
    SELECT telegram_id FROM telegram_users WHERE username = ?
"""
select_complaint = """
    SELECT count FROM complaint WHERE telegram_id_bad_user = ?
"""
select_complaint_check = """
    SELECT telegram_id FROM complaint WHERE telegram_id = ? AND telegram_id_bad_user = ?
"""
