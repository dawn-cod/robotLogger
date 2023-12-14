import pymysql

class Connection():
    def __init__(self):
        self.connection = pymysql.connect(host='10.10.168.55', port=3308, user='chenhao', password='chenhao@Wct0323')
        

    def exc(self, sql, *args, **kwargs):
        with self.connection:
            self.cur = self.connection.cursor()
            self.cur.execute(sql, *args, **kwargs)
            results = self.cur.fetchall()
            return results

