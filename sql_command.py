import sqlite3
import config

conn = sqlite3.connect(config.expl) #VMESTO "config.expl" NUGNO PODSTAVIT PYT' K SQL FAILU
cursor = conn.cursor()
#вывод всех компаний
cursor.execute("""
SELECT Название
  FROM Заведения
  ORDER BY Название
""")
all_company = cursor.fetchall()



#вывод блюд определенной компании
company = "KFC"
cursor.execute("""
SELECT Блюдо
FROM '""" + str(company) +"' ORDER BY Блюдо")
price = cursor.fetchall()


#вывод все варианты кухни
cursor.execute("""
SELECT Название
  FROM Кухня
  ORDER BY Название;
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
SELECT *
  FROM KFC
 WHERE Блюдо = '""" + str(bludo) +"'")
info_food = cursor.fetchall()





conn.close()


