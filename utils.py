# -*- coding: utf-8 -*-
import shelve
from config import shelve_name


def set_basket(user_id):
    """
    Записываем юзера в хранилище.
    :param user_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        print('Пользователь', user_id, 'создал корзину')
        storage[user_id] = {}


def get_basket(user_id):
    """
    Получем словарь товаров в корзине пользователя.
    :param user_id: id пользовател
    :return: (dict) Товары в хранилище
    """
    with shelve.open(shelve_name) as storage:
        print('Корзина пользователя', user_id)
        return storage.get(user_id, {})


def add_to_basket(user_id, product):
    """
    Добавляем выбранный товар в корзину юзера.
    :param user_id: id юзера
    :param product: товар, добавляемый в хранилище,
    """
    with shelve.open(shelve_name) as storage:
        print('Пользователь', user_id, 'добавил', product, 'в корзину')
        temp = storage[user_id]
        if temp.get(product):
            temp[product] += 1
        else:
            temp.update({product : 1})
        storage[user_id] = temp


def del_from_basket(user_id, product):
    """
    Удаляем выбранный товар из корзины юзера.
    :param user_id: id юзера
    :param product: товар, удаляемый из хранилища
    """
    with shelve.open(shelve_name) as storage:
        temp = storage[user_id]
        try:
            print('Пользователь', user_id, 'удалил из корзины', product)
            temp.pop(product)
        except:
            print('\tПользователь', user_id, 'пытается удалить несуществующий', product)
        storage[user_id] = temp


def remove_amount(user_id, product):
    """
    Уменьшаем на 1 количество товара в корзине.
    :param user_id: id юзера
    :param product: товар, количество которого уменьшается
    """
    with shelve.open(shelve_name) as storage:
        print('Пользователь', user_id, 'удалил единицу', product, 'из корзины')
        temp = storage[user_id]
        if temp.get(product):
            temp[product] -= 1
        else:
            print('\tПользователь', user_id, 'пытается удалить несуществующий', product)
        storage[user_id] = temp


def item_amount(user_id, product):
    """
    Возвращает количество выбранного товара.
    :param user_id: id пользователя
    :param product: товар в хранилище
    :return: (int) количество товара
    """
    with shelve.open(shelve_name) as storage:
        return storage[user_id].get(product, 0)


def del_user_basket(user_id):
    """
    Очищаем корзину текущего пользователя.
    :param user_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        try:
            print('Корзина пользователя', user_id, 'удалена')
            del storage[user_id]
        except:
            print('\tПользователь {user} пытается удалить несуществующую корзину', user_id)