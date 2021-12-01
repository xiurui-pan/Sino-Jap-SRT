import json
import pymysql as sql

def load_ua():
    ua_list = []
    with open("./config/ua.txt", "r") as f:
        for line in f.readlines():
            if line:
                if line[0] != '#':
                    ua_list.append(line.strip().strip("\n").strip("\r").strip("\""))
    return ua_list

def load_mysql():
    with open("./config/sql_login.json") as f:
        sql_login = json.loads(f.read())
    return sql.connect(**sql_login)

def load_settings():
    with open("./config/settings.json") as f:
        settings = json.loads(f.read())
    return settings