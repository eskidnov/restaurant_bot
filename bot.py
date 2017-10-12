# -*- coding: utf-8 -*-
import telebot
import config
import utils

bot = telebot.TeleBot(config.token)

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

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    print('Бот запущен пользователем', user_id)
    utils.set_basket(user_id)
    bot.send_message(message.chat.id, config.main_menu, parse_mode='markdown', reply_markup=main_menu_keyboard)

# ВОЗВРАТ В МЕНЮ

@bot.message_handler(func=lambda item: item.text == config.back_button, content_types=['text'])
def back(message):
    print('Пользователь', message.from_user.id, 'вернулся в основное меню')
    bot.send_message(message.chat.id, config.main_menu, reply_markup=main_menu_keyboard)

# ОПИСАНИЕ

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[0], content_types=['text'])
def description(message):
    print('Пользователь', message.from_user.id, 'открыл "Описание"')
    bot.send_message(message.chat.id, config.description, reply_markup=back_keyboard)

# ФОТОГРАФИИ

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[1], content_types=['text'])
def photos(message):
    print('Пользователь', message.from_user.id, 'открыл "Фотографии"')
    bot.send_message(message.chat.id, config.photos, reply_markup=back_keyboard)

# МЕНЮ

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[2], content_types=['text'])
def menu(message):
    print('Пользователь', message.from_user.id, 'открыл "Меню"')
    bot.send_message(message.chat.id, config.menu, reply_markup=menu_keyboard)

@bot.callback_query_handler(func=lambda query: 'menu' in query.data)
def menu_section(query):
    bot.answer_callback_query(query.id)

    user_id = str(query.from_user.id)
    section_number = int(query.data[5:])
    section = sorted_sections_list[section_number]
    print('Пользователь', user_id, 'открыл "Раздел меню', section_number+1, '" в "Меню"')

    bot.edit_message_text(section, query.message.chat.id, query.message.message_id)
    # ЗДЕСЬ НУЖНА ВЫГРУЗКА БЛЮД РАЗДЕЛА ИЗ БД
    for item in config.menu_keyboard[section]:
        bot.send_message(query.message.chat.id, item, reply_markup=amount_keyboard(user_id, item))

@bot.callback_query_handler(func=lambda query: '->' in query.data)
def amount_inc(query):
    bot.answer_callback_query(query.id)

    user_id = str(query.from_user.id)
    item = query.data.split('_')[1]

    utils.add_to_basket(user_id, item)
    if 'b->' in query.data:
        bot.edit_message_reply_markup(query.message.chat.id, query.message.message_id,
                                      reply_markup=amount_keyboard(user_id, item, basket=True))
    else:
        bot.edit_message_reply_markup(query.message.chat.id, query.message.message_id,
                                      reply_markup=amount_keyboard(user_id, item))

@bot.callback_query_handler(func=lambda query: '<-' in query.data)
def amount_dec(query):
    bot.answer_callback_query(query.id)

    user_id = str(query.from_user.id)
    chat_id = query.message.chat.id
    item = query.data.split('_')[1]

    utils.remove_amount(user_id, item)
    if not utils.item_amount(user_id, item):
        utils.del_from_basket(user_id, item)
        if 'b<-' in query.data:
            bot.delete_message(chat_id, query.message.message_id)
            bot.send_message(chat_id, config.empty_basket)
        else:
            bot.edit_message_reply_markup(chat_id, query.message.message_id,
                                          reply_markup=amount_keyboard(user_id, item))
    elif 'b<-' in query.data:
        bot.edit_message_reply_markup(chat_id, query.message.message_id,
                                      reply_markup=amount_keyboard(user_id, item, basket=True))
    else:
        bot.edit_message_reply_markup(chat_id, query.message.message_id,
                                      reply_markup=amount_keyboard(user_id, item))

@bot.callback_query_handler(func=lambda query: query.data == 'to_basket')
def to_basket(query):
    bot.answer_callback_query(query.id)
    basket(str(query.from_user.id), query.message.chat.id)

# КОРЗИНА

def basket(user_id, chat_id):
    _basket = utils.get_basket(user_id)
    print('Пользователь', user_id, 'открыл "Корзина"')
    print(utils.get_basket(user_id))

    if not _basket:
        bot.send_message(chat_id, config.basket)
        bot.send_message(chat_id, config.empty_basket)
    else:
        bot.send_message(chat_id, config.basket, reply_markup=pay_keyboard)
        for item in _basket:
            bot.send_message(chat_id, item, reply_markup=amount_keyboard(user_id, item, basket=True))

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[3], content_types=['text'])
def _basket(message):
    basket(str(message.from_user.id), message.chat.id)

@bot.callback_query_handler(func=lambda query: query.data[:6] == 'amount')
def item_amount(query):
    print(utils.get_basket(str(query.from_user.id)))
    bot.answer_callback_query(callback_query_id=query.id)

@bot.callback_query_handler(func=lambda query: query.data[:6] == 'remove')
def remove(query):
    bot.answer_callback_query(callback_query_id=query.id)

    utils.del_from_basket(str(query.from_user.id), query.data[7:])
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
def pay_newAPI(message):
    print('Пользователь', message.from_user.id, 'оформляет заказ через Telegram')
    bot.send_message(message.chat.id, config.view_basket, reply_markup=back_keyboard)
    msg = ''
    price = 0
    for item in utils.get_basket(str(message.from_user.id)):
        # НАДЕЮСЬ, ЧТО НУЖНО ДЕЛАТЬ ПОЯСНЕНИЙ НЕ ТРЕБУЕТСЯ, НО ЕСЛИ ЧТО, ЗВОНИ :-*
        amount = utils.item_amount(str(message.from_user.id), item)
        msg += ' - ' + item + ': ' + str(amount) + '\n'
        price += amount * 10000
    prices = [telebot.types.LabeledPrice(config.check_num, price)]

    new_pay = telebot.types.InlineKeyboardMarkup(row_width=1)
    new_pay.add(telebot.types.InlineKeyboardButton(text=config.pay, pay=True))

    bot.send_invoice(chat_id=message.chat.id,
                     title=config.check_num,
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
    shipping_options = []

    shipping_option = telebot.types.ShippingOption('delivery', 'Доставка курьером')
    shipping_option.add_price(telebot.types.LabeledPrice('Курьер', 10000))
    shipping_options.append(shipping_option)

    shipping_option = telebot.types.ShippingOption('sam', 'Самовывоз')
    shipping_option.add_price(telebot.types.LabeledPrice('Самовывоз', 0))
    shipping_options.append(shipping_option)

    bot.answer_shipping_query(shipping_query_id=shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message=config.error_answer_query)


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                  ok=True,
                                  error_message=config.error_pre_checkout)


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    print('Пользователь', message.from_user.id, 'оформил заказ')
    for item in utils.get_basket(str(message.from_user.id)):
        utils.del_from_basket(str(message.from_user.id), item)
    bot.send_message(chat_id=message.chat.id,
                     text=config.successful_payment.format(message.successful_payment.total_amount / 100,
                                                           message.successful_payment.currency),
                     parse_mode='Markdown', reply_markup=main_menu_keyboard)

if __name__ == '__main__':

    main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = (telebot.types.KeyboardButton(text=button_text) for button_text in config.main_menu_keyboard)
    main_menu_keyboard.add(*buttons)

    back_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_keyboard.add(telebot.types.KeyboardButton(text=config.back_button))

    def amount_keyboard(user_id, item, basket=False):
        if basket:
            amount = telebot.types.InlineKeyboardMarkup()
            amount.row(telebot.types.InlineKeyboardButton(text='<-', callback_data='b<-_' + item),
                       telebot.types.InlineKeyboardButton(text=str(utils.item_amount(user_id, item)),
                                                          callback_data='amount_' + item),
                       telebot.types.InlineKeyboardButton(text='->', callback_data='b->_' + item))
            amount.add(telebot.types.InlineKeyboardButton(text=config.del_from_basket,
                                                          callback_data='remove_' + item))
        elif utils.item_amount(user_id, item):
            amount = telebot.types.InlineKeyboardMarkup()
            amount.row(telebot.types.InlineKeyboardButton(text='<-', callback_data='<-_' + item),
                       telebot.types.InlineKeyboardButton(text=str(utils.item_amount(user_id, item)),
                                                          callback_data='amount_' + item),
                       telebot.types.InlineKeyboardButton(text='->', callback_data='->_' + item))
            amount.add(telebot.types.InlineKeyboardButton(text=config.to_basket, callback_data='to_basket'))
        else:
            amount = telebot.types.InlineKeyboardMarkup()
            amount.row(telebot.types.InlineKeyboardButton(text='<-', callback_data='<-_' + item),
                       telebot.types.InlineKeyboardButton(text=str(utils.item_amount(user_id, item)),
                                                          callback_data='amount_' + item),
                       telebot.types.InlineKeyboardButton(text='->', callback_data='->_' + item))

        return amount

    ### ЗДЕСЬ НУЖНА ВЫГРУЗКА РАЗДЕЛОВ ИЗ БД
    menu_keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    sorted_sections_list = list(config.menu_keyboard)
    sorted_sections_list.sort()
    buttons = (telebot.types.InlineKeyboardButton(text=button_text, callback_data='menu_' + str(i))
               for i, button_text in enumerate(sorted_sections_list))
    menu_keyboard.add(*buttons)
    ###

    pay_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    pay_keyboard.add(telebot.types.KeyboardButton(text=config.pay_button),
                     telebot.types.KeyboardButton(text=config.back_button))

    hidden_keyboard = telebot.types.ReplyKeyboardRemove()

    bot.polling(none_stop=True)