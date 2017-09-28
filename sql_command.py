import sqlite3
import config

conn = sqlite3.connect(config.expl)
cursor = conn.cursor()

cursor.execute("""
SELECT Название,Номер,Описание,Лого,Время,Европейская,Фастфуд,Азиатская,Кавказская
  FROM Заведения
""")
results = cursor.fetchall()
print (results)


conn.close()