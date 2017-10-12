import sqlite3

import config
import sql_command

#print (sql_command.all_company)                         #VIOD SPISKOV
#print (sql_command.price)
#print (sql_command.kitchen)
#print (sql_command.kitchen_price)
#print (sql_command.info_food)


class sql:
    def tovars(self):
        conn = sqlite3.connect(config.expl)
        cursor = conn.cursor()
        company = "KFC"
        cursor.execute("""
        SELECT Блюдо
        FROM '""" + str(company) + "' ORDER BY Блюдо")

        tovars = cursor.fetchall()
        conn.close()
        return tovars

    def kitchen(self):
        conn = sqlite3.connect(config.expl)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT Название
        FROM Кухня
        ORDER BY Название;
        """)
        kitchen = cursor.fetchall()
        conn.close()
        return kitchen
    def bludo_po_kuhne(self, kitchen_vibor):
        conn = sqlite3.connect(config.expl)
        cursor = conn.cursor()
        self.kitchen_vibor = "Фастфуд"
        cursor.execute("""
        SELECT Блюдо
          FROM KFC
          WHERE Кухня = '""" + str(kitchen_vibor) + "'")
        kitchen_price = cursor.fetchall()
        conn.close()
        return kitchen_price
    def bludo_info(self, bludo):
        conn = sqlite3.connect(config.expl)
        cursor = conn.cursor()
        # Вывод всей информации о блюде
        self.bludo = "Биггер"
        cursor.execute("""
        SELECT *
          FROM KFC
         WHERE Блюдо = '""" + str(bludo) + "'")
        info_food = cursor.fetchall()
        conn.close()
        return info_food






conn = sqlite3.connect(config.expl)
cursor = conn.cursor()

for i in sql_command.kitchen:
    kitchen = str(i)
    #print((kitchen[2:-3]))                             # VIVOD KUHNI
    cursor.execute("""
    SELECT Блюдо
      FROM KFC
      WHERE Кухня = '""" + (kitchen[2:-3]) + "'")
    kitchen_price = cursor.fetchall()


for x in kitchen_price:
    name = str(x)
    #print(name[2:-3])                              #VIVOD TOVARA
    bludo = "Биггер"
    cursor.execute("""
        SELECT Блюдо,
               Изображение,
               Описание,
               Состав,
               Стоимость,
               Кухня
          FROM KFC
         WHERE Блюдо = '""" + name[2:-3] + "'")
    info_food = cursor.fetchall()

for y in info_food:
        #print (y)                                  #VIVOD OPICANIUA TOVARA

        menu_keyboard = {
            'Раздел меню 1': [
                'Блюдо 1',
                'Блюдо 2',
            ]
        }


menu_keyboard = {
    'Раздел меню 1' : [
        'Блюдо 1',
        'Блюдо 2',
    ],
    'Раздел меню 2' : [
        'Блюдо 3',
        'Блюдо 4',
    ]
}








conn.close()