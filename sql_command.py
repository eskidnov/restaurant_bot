import sqlite3
import config

conn = sqlite3.connect(config.expl)
cursor = conn.cursor()
#вывод всех компаний
cursor.execute("""
SELECT Название
  FROM Заведения
""")
all_company = cursor.fetchall()



#вывод блюд определенной компании
company = "KFC"
cursor.execute("""
SELECT Блюдо
FROM '""" + str(company) +"'")
price = cursor.fetchall()


#вывод все варианты кухни
cursor.execute("""
SELECT Название
  FROM Кухня;
  """)
kitchen = cursor.fetchall()

#Вывод всех товаров определенной кухни
kitchen_vibor = "Фастфуд" # dla primera
cursor.execute("""
SELECT Блюдо
  FROM KFC
  WHERE Кухня = '""" + str(kitchen_vibor) +"'")
kitchen_price = cursor.fetchall()

#Вывод всей информации о блюде
bludo = "Биггер"
cursor.execute("""
SELECT Блюдо,
       Изображение,
       Описание,
       Состав,
       Стоимость,
       Кухня
  FROM KFC
 WHERE Блюдо = '""" + str(bludo) +"'")
info_food





conn.close()


