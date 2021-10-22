from utils import core, debugger
# import pymysql as sql
import codecs, json


def pps(input: str) -> str:
    input = input.replace("'", "''")
    return input

class Sqldb:

    def __init__(self):

        self.conn = core.load_mysql()
        debugger.INFO("database connected.")


    def generate(self, filename: str, table_name: str) -> bool:
        """Insert all the data of "filename" into mysql

        :param filename: name of the json file
        :return: success or not
        """
        fp = codecs.open(filename, 'r', 'utf-8')
        contents = json.load(fp, strict=False)
        with self.conn.cursor() as cur:
            for index, article in enumerate(contents):
                if "body" not in article:
                    article["body"] = "NULL"
                sql = """INSERT INTO {}(title, time, url, article) 
                         VALUES('{}', '{}', '{}', '{}')
                      """.format(table_name, pps(article["title"]), pps(article["time"]), pps(article["url"]), pps(article["body"]))
                cur.execute(sql)
                self.conn.commit()
                # try:
                #     cur.execute(sql)
                #     self.conn.commit()
                # except:
                #     self.conn.rollback()
                #     fp.close()
                #     return False
        fp.close()
        return True


    def close(self):
        debugger.INFO("database closed")
        self.conn.close()