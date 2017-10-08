import sqlite3

import config
import sql_command

print (sql_command.all_company)                         #VIOD SPISKOV
print (sql_command.price)
print (sql_command.kitchen)
print (sql_command.kitchen_price)
print (sql_command.info_food)


conn = sqlite3.connect(config.expl)
cursor = conn.cursor()

for i in sql_command.kitchen:
    kitchen = str(i)
    print((kitchen[2:-3]))                             # VIVOD KUHNI
    cursor.execute("""
    SELECT Блюдо
      FROM KFC
      WHERE Кухня = '""" + (kitchen[2:-3]) + "'")
    kitchen_price = cursor.fetchall()
    for x in kitchen_price:
        name = str(x)
        print(name[2:-3])                              #VIVOD TOVARA
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
            print (y)                                  #VIVOD OPICANIUA TOVARA

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