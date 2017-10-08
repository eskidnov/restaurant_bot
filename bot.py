# -*- coding: utf-8 -*-
import sqlite3
import telebot
import config
import utils
import sql_command

bot = telebot.TeleBot(config.token)

main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
buttons = (telebot.types.KeyboardButton(text=button_text) for button_text in config.main_menu_keyboard)
main_menu_keyboard.add(*buttons)

back_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
back_keyboard.add(telebot.types.KeyboardButton(text=config.back_button))

# Возможно полезная херня с сортированным вложенным меню
# # Создание сортированного списка разделов меню
# #sorted_sections_list = sorted(config.menu_keyboard.items(), key=lambda t: t[0]) # Список тьюплов ключ-значение
# sorted_sections_list = sorted(config.menu_keyboard, key=lambda t: t[0])
# # Создание словаря клавиатур (клавиатура для каждого раздела)
# menu_keyboard = [telebot.types.InlineKeyboardMarkup(row_width=2) for i in range(len(sorted_sections_list)+1)]
# ## Создание сортированного словаря клавиатур (сортировка по названию раздела)
# #menu_keyboard = OrderedDict(sorted(keyboards_dict.items(), key=lambda t: t[0]))
# # Создание кнопок для каждой клавиатуры
# for i, item in enumerate(sorted_sections_list, 1):
#     buttons = (telebot.types.InlineKeyboardButton(text=button_text, callback_data='menu_'+str(i)+'_'+str(j))
#                for j, button_text in enumerate(config.menu_keyboard[item], 1))
#     menu_keyboard[i].add(*buttons)
# # Добавление клавиатуры для разделов
# buttons = (telebot.types.InlineKeyboardButton(text=button_text, callback_data='menu_'+str(i))
#            for i, button_text in enumerate(config.menu_keyboard, 1))
# menu_keyboard[0].add(*buttons)

#### ЗДЕСЬ НУЖНА ВЫГРУЗКА РАЗДЕЛОВ ИЗ БД
global keyboard
conn = sqlite3.connect(config.expl)
cursor = conn.cursor()
for i in sql_command.kitchen:
    kitchen = str(i)

    cursor.execute("""
    SELECT Блюдо
      FROM KFC
      WHERE Кухня = '""" + (kitchen[2:-3]) + "'")
    kitchen_price = str(cursor.fetchall())
    kitchen_price = kitchen_price[2:-3]
    global keyboard
    keyboard = {
        sql_command.kitchen: [
            'Блюдо 3',
            'Блюдо 4',
        ],
        'Раздел меню 2': [
            'Блюдо 3',
            'Блюдо 4', ]
    }
conn.close()
menu_keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
sorted_sections_list = list(keyboard)
sorted_sections_list.sort()
buttons = (telebot.types.InlineKeyboardButton(text=button_text, callback_data='menu_' + str(i))
           for i, button_text in enumerate(sorted_sections_list))
menu_keyboard.add(*buttons)


####

def amount(user_id, item):
    amount_keyboard = telebot.types.InlineKeyboardMarkup()
    amount_keyboard.row(telebot.types.InlineKeyboardButton(text='<-', callback_data='a<-_' + item),
                        telebot.types.InlineKeyboardButton(text=str(utils.item_amount(user_id, item)),
                                                           callback_data='amount_' + item),
                        telebot.types.InlineKeyboardButton(text='->', callback_data='a->_' + item))
    return amount_keyboard


def basket(user_id, item):
    basket_keyboard = telebot.types.InlineKeyboardMarkup()
    basket_keyboard.row(telebot.types.InlineKeyboardButton(text='<-', callback_data='b<-_' + item),
                        telebot.types.InlineKeyboardButton(text=str(utils.item_amount(user_id, item)),
                                                           callback_data='amount_' + item),
                        telebot.types.InlineKeyboardButton(text='->', callback_data='b->_' + item))
    basket_keyboard.add(telebot.types.InlineKeyboardButton(text=config.del_from_basket,
                                                           callback_data='remove_' + item))
    return basket_keyboard


pay_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
pay_keyboard.add(telebot.types.KeyboardButton(text=config.pay_button),
                 telebot.types.KeyboardButton(text=config.back_button))

hidden_keyboard = telebot.types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    print('Бот запущен пользователем', user_id)
    utils.set_basket(user_id)
    bot.send_message(chat_id=message.chat.id, text=config.main_menu, parse_mode='markdown',
                     reply_markup=main_menu_keyboard)


# ВОЗВРАТ В МЕНЮ

@bot.message_handler(func=lambda item: item.text == config.back_button, content_types=['text'])
def back(message):
    print('Пользователь', message.from_user.id, 'вернулся в основное меню')
    bot.send_message(chat_id=message.chat.id, text=config.main_menu, reply_markup=main_menu_keyboard)


# ОПИСАНИЕ

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[0], content_types=['text'])
def description(message):
    print('Пользователь', message.from_user.id, 'открыл "Описание"')
    bot.send_message(chat_id=message.chat.id, text=config.description, reply_markup=back_keyboard)


# ФОТОГРАФИИ

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[1], content_types=['text'])
def photos(message):
    print('Пользователь', message.from_user.id, 'открыл "Фотографии"')
    bot.send_message(chat_id=message.chat.id, text=config.photos, reply_markup=back_keyboard)


# МЕНЮ

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[2], content_types=['text'])
def menu(message):
    print('Пользователь', message.from_user.id, 'открыл "Меню"')
    bot.send_message(chat_id=message.chat.id, text=config.menu, reply_markup=menu_keyboard)


@bot.callback_query_handler(func=lambda query: query.data[:4] == 'menu' and len(query.data.split('_')) == 2)
def menu_section(query):
    section_number = int(query.data.split('_')[1])
    print('Пользователь', query.from_user.id, 'открыл "Раздел меню', section_number + 1, '" в "Меню"')
    bot.answer_callback_query(callback_query_id=query.id)
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                          text=sorted_sections_list[section_number])
    # ЗДЕСЬ НУЖНА ВЫГРУЗКА БЛЮД РАЗДЕЛА ИЗ БД
    for item in config.menu_keyboard[sorted_sections_list[section_number]]:
        to_basket = amount(str(query.from_user.id), item)
        if utils.item_amount(str(query.from_user.id), item):
            to_basket.add(telebot.types.InlineKeyboardButton(text=config.to_basket,
                                                             callback_data='to_basket_' + item))
        bot.send_message(chat_id=query.message.chat.id, text=item, reply_markup=to_basket)


@bot.callback_query_handler(func=lambda query: query.data[:4] == 'menu' and len(query.data.split('_')) == 3)
def menu_dishes(query):
    section_number, item_number = (int(elem) for elem in query.data.split('_')[1:])
    print('Пользователь', query.from_user.id, 'открыл "Блюдо', item_number,
          '" в "Раздел меню', section_number + 1, '" в "Меню"')
    bot.answer_callback_query(callback_query_id=query.id)
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                          text=config.menu_keyboard[sorted_sections_list[section_number - 1]][item_number - 1])


@bot.callback_query_handler(func=lambda query: query.data[:3] == 'a->')
def amount_inc(query):
    bot.answer_callback_query(callback_query_id=query.id)
    utils.add_to_basket(str(query.from_user.id), query.data[4:])
    to_basket = amount(str(query.from_user.id), query.data[4:])
    to_basket.add(telebot.types.InlineKeyboardButton(text=config.to_basket,
                                                     callback_data='to_basket_' + query.data[4:]))
    bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  reply_markup=to_basket)


@bot.callback_query_handler(func=lambda query: query.data[:3] == 'a<-')
def amount_inc(query):
    bot.answer_callback_query(callback_query_id=query.id)
    utils.remove_amount(str(query.from_user.id), query.data[4:])
    to_basket = amount(str(query.from_user.id), query.data[4:])
    if utils.item_amount(str(query.from_user.id), query.data[4:]):
        to_basket.add(telebot.types.InlineKeyboardButton(text=config.to_basket,
                                                         callback_data='to_basket_' + query.data[4:]))
    else:
        utils.del_from_basket(str(query.from_user.id), query.data[4:])
    bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  reply_markup=to_basket)


@bot.callback_query_handler(func=lambda query: query.data[:9] == 'to_basket')
def to_basket(query):
    bot.answer_callback_query(callback_query_id=query.id)
    user_id = str(query.from_user.id)
    _basket = utils.get_basket(user_id)
    print('Пользователь', user_id, 'открыл "Корзина"')
    print(utils.get_basket(user_id))
    if not _basket:
        bot.send_message(query.message.chat.id, config.basket)
        bot.send_message(chat_id=query.message.chat.id, text=config.empty_basket)
    else:
        bot.send_message(query.message.chat.id, config.basket, reply_markup=pay_keyboard)
        for item in _basket:
            bot.send_message(chat_id=query.message.chat.id, text=item, reply_markup=basket(user_id, item))


# КОРЗИНА

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[3], content_types=['text'])
def __basket(message):
    print('Пользователь', message.from_user.id, 'открыл "Корзина"')
    user_id = str(message.from_user.id)
    _basket = utils.get_basket(user_id)
    if not _basket:
        bot.send_message(message.chat.id, config.basket)
        bot.send_message(chat_id=message.chat.id, text=config.empty_basket)
    else:
        bot.send_message(message.chat.id, config.basket, reply_markup=pay_keyboard)
        for item in _basket:
            bot.send_message(chat_id=message.chat.id, text=item, reply_markup=basket(user_id, item))


@bot.callback_query_handler(func=lambda query: query.data[:3] == 'b->')
def amount_inc(query):
    bot.answer_callback_query(callback_query_id=query.id)
    utils.add_to_basket(str(query.from_user.id), query.data[4:])
    bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  reply_markup=basket(str(query.from_user.id), query.data[4:]))


@bot.callback_query_handler(func=lambda query: query.data[:3] == 'b<-')
def amount_inc(query):
    bot.answer_callback_query(callback_query_id=query.id)
    utils.remove_amount(str(query.from_user.id), query.data[4:])
    if not utils.item_amount(str(query.from_user.id), query.data[4:]):
        utils.del_from_basket(str(query.from_user.id), query.data[4:])
        bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    else:
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                      reply_markup=basket(str(query.from_user.id), query.data[4:]))
    if not utils.get_basket(str(query.from_user.id)):
        bot.send_message(chat_id=query.message.chat.id, text=config.empty_basket)


@bot.callback_query_handler(func=lambda query: query.data[:6] == 'amount')
def item_amount(query):
    print(utils.get_basket(str(query.from_user.id)))
    bot.answer_callback_query(callback_query_id=query.id)


@bot.callback_query_handler(func=lambda query: query.data[:6] == 'remove')
def remove(query):
    utils.del_from_basket(str(query.from_user.id), query.data[7:])
    bot.answer_callback_query(callback_query_id=query.id)
    bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    print(utils.get_basket(str(query.from_user.id)))
    if not utils.get_basket(str(query.from_user.id)):
        bot.send_message(chat_id=query.message.chat.id, text=config.empty_basket)


# ОФОРМЛЕНИЕ ЗАКАЗА

@bot.message_handler(func=lambda item: item.text == config.pay_button, content_types=['text'])
def payment(message):
    print('Пользователь', message.from_user.id, 'начал оформление заказа')
    pay_way_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    pay_way_keyboard.add(telebot.types.KeyboardButton(config.pay_way[0]),
                         telebot.types.KeyboardButton(config.pay_way[1]),
                         telebot.types.KeyboardButton(config.back_button))
    bot.send_message(message.chat.id, config.choose_pay_way, reply_markup=pay_way_keyboard)


# ЗДЕСЬ НУЖНА ВЫГРУЗКА ДАННЫХ ПО КАЖДОМУ ПРОДУКТУ ИЗ КОРЗИНЫ ИЗ БД
@bot.message_handler(func=lambda item: item.text == config.pay_way[0], content_types=['text'])
def telega(message):
    print('Пользователь', message.from_user.id, 'оформляет заказ через Telegram')
    bot.send_message(message.chat.id, config.view_basket, reply_markup=back_keyboard)
    msg = ''
    price = 0
    for item in utils.get_basket(str(message.from_user.id)):
        # НАДЕЮСЬ, ЧТО НУЖНО ДЕЛАТЬ ПОЯСНЕНИЙ НЕ ТРЕБУЕТСЯ, НО ЕСЛИ ЧТО, ЗВОНИ :-*
        amount = utils.item_amount(str(message.from_user.id), item)
        msg += '- ' + item + ': ' + str(amount) + '\n'
        price += amount * 100
    prices = {'Заказ №12345': [telebot.types.LabeledPrice('Заказ №12345', price)]}
    new_pay = telebot.types.InlineKeyboardMarkup(row_width=1)
    new_pay.add(telebot.types.InlineKeyboardButton(text=config.pay, pay=True))
    bot.send_invoice(chat_id=message.chat.id,
                     title='Заказа №12345',
                     description=msg,
                     invoice_payload='invoice',
                     provider_token=config.provider_token,
                     start_parameter='invoice',
                     currency='rub',
                     prices=prices,
                     need_name=True,
                     need_phone_number=True,
                     need_shipping_address=True,
                     is_flexible=True,
                     reply_markup=new_pay)


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    shipping_options = [
        telebot.types.ShippingOption('delivery', 'Доставка курьером').add_price([
            telebot.types.LabeledPrice('Курьер', 10000)
        ]),
        telebot.types.ShippingOption('sam', 'Самовывоз').add_price([
            telebot.types.LabeledPrice('Самовывоз', 0)
        ]),
    ]
    bot.answer_shipping_query(shipping_query_id=shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message=config.error_answer_query)


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                  ok=True,
                                  error_message=config.error_pre_checkout)


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(chat_id=message.chat.id,
                     text=payment.successful_payment.format(message.successful_payment.total_amount / 100,
                                                            message.successful_payment.currency),
                     parse_mode='Markdown')


if __name__ == '__main__':
    bot.polling(none_stop=True)
