import sqlite3

table_name = "spend"

class DB:
  def __init__(self, db_name):
      self.conn = sqlite3.connect(db_name)
      self.cursor = self.conn.cursor()
      if table_name not in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
        self._create_db(db_name)
    
  def _create_db(self, db_name):
    self.cursor.execute("CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, value INT NOT NULL, datetime TEXT NOT NULL)".format(table_name))
    self.conn.commit()
  
  def create(self, data):
    self.cursor.execute("INSERT INTO {} (value, datetime) VALUES({},{})".format(table_name, data["value"], data["datetime"]))
    self.conn.commit()
    return(self.read_last())

  def create_multi(self, datas):
    query = "INSERT INTO {} (value, datetime) VALUES ".format(table_name)
    for data in datas:
      query += "({},{}),".format(data["value"], data["datetime"])
    query = query[:-1]
    print(query)
    self.cursor.execute(query)
    self.conn.commit()
    return
  
  def read_all(self):
    l = self.cursor.execute("SELECT * FROM {}".format(table_name)).fetchall()
    return(list(map(self._tuple2dict, l)))#list transform the iterator to a list maybe not needed
  
  def read_last(self):
    data = self.cursor.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(table_name)).fetchall()[0]
    return(self._tuple2dict(data))
    
  def _tuple2dict(self, tup):
    return({"id":tup[0], "value":tup[1], "datetime":tup[2]})
    
if __name__ == "__main__":
  db = DB("test.db")
  print(db.create({"id":None, "value":122, "datetime":"2022"}))
  db.create_multi([{"id":None, "value":122, "datetime":"2023"},{"id":None, "value":122, "datetime":"2024"}])
  print(db.read_all())
  