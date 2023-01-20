import sqlite3
from datetime import datetime

table_name = "spend"

class DB:
  def __init__(self, db_name):
      self.conn = sqlite3.connect(db_name)
      self.cursor = self.conn.cursor()
      if table_name not in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
        self._create_db(db_name)

  def _create_db(self, db_name):
    self.cursor.execute("CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, value INT NOT NULL, datetime datetime NOT NULL)".format(table_name))
    self.conn.commit()

  ##CREATE

  def create(self, data):
    self.cursor.execute("INSERT INTO {} (value, datetime) VALUES(?,?)".format(table_name), (data["value"], data["datetime"]))
    self.conn.commit()
    return(self.read_last())

  def create_multi(self, datas):
    result = []
    for data in datas:
      result.append(self.create(data))
    return(result)

  ##READ

  def read_all(self):
    l = self.cursor.execute("SELECT * FROM {}".format(table_name)).fetchall()
    return(list(map(self._tuple2dict, l)))#list transform the iterator to a list maybe not needed

  def read_last(self):
    data = self.cursor.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(table_name)).fetchall()[0]
    return(self._tuple2dict(data))

  def read_month(self, month, year):
    pass

  def read_from_to(self, fr, to):
    pass

  def read(self, id):
    data = self.cursor.execute("SELECT * FROM {} WHERE id=? LIMIT 1".format(table_name),(id,)).fetchall()[0]
    return(self._tuple2dict(data))

  ##UPDATE

  def update(self, data):
    self.cursor.execute("UPDATE {} SET value=?, datetime=? WHERE id=?".format(table_name),(data['value'], data['datetime'], data['id']))
    self.conn.commit()
    return(self.read(data['id']))

  def update_multi(self,datas):
    result=[]
    for data in datas:
      result.append(self.update(data))
    return(result)

  ##DELETE

  def delete(self,id):
    self.cursor.execute("DELETE FROM {} WHERE id=?".format(table_name), id) 



  def _tuple2dict(self, tup):
    return({"id":tup[0], "value":tup[1], "datetime":self._text2datetime(tup[2])})

  def _text2datetime(self, text):
    return(datetime.fromisoformat(text))

if __name__ == "__main__":
  db = DB("test.db")
  #db.create({"id":None, "value":122, "datetime":datetime.now()})
  #db.create_multi([{"id":None, "value":122, "datetime":datetime.now()},{"id":None, "value":122, "datetime":datetime.now()}])
  datas = db.read_all()
  print(datas[-3]['id'])
  print(datas)
  data = datas[-3]
  data['value'] += 100
  print("\n")
  db.update(data)
  datas = db.read_all()
  print(datas)

  
  