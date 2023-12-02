import keyword
import json


class Dict2Obj:
    """
    При создании экземпляра класса на вход подаётся словарь. Его ключи
    становятся атрибутами экземпляра, значения - значениями атрибутов.
    К атрибутам любой вложенности можно обращаться через точку.
    К названия атрибутов, являющихся ключевыми словами python, в конце
    названия добавляет '_'.
    """
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, (list, tuple)):
                setattr(self, self.key_rename(key), [
                    Dict2Obj(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, self.key_rename(key), Dict2Obj(
                    value) if isinstance(value, dict) else value)

    @staticmethod
    def key_rename(key):
        """
        Добавляет к ключу словаря '_', если он является ключевым словом
        """
        if keyword.iskeyword(key):
            return key + '_'
        return key


class Advert(Dict2Obj):
    """
    Динамически создаёт атрибуты экземпляра класса из атрибутов JSON-объекта.
    Отличается от класса Dict2Obj тем, что имеет свойство price:
    проверяет, что значение не отрицательное и при создании объекта и при
    присваивании
    """
    def __init__(self, dictionary):
        super().__init__(dictionary)
        if not hasattr(self, 'title'):
            raise ValueError('Атрибут title - обязательный')
        if hasattr(self, '_price'):
            if self._price < 0:
                raise ValueError('must be >= 0')
        else:
            self._price = 0

    def key_rename(self, key):
        """
        Дополняет родительский метод, меняя атрибут 'price' на защищённый
        атрибут '_price'
        """
        if super().key_rename(key) == 'price':
            return '_price'
        return super().key_rename(key)

    @property
    def price(self):
        """
        защищённый вызов 'price'
        """
        return self._price

    @price.setter
    def price(self, price):
        """
        защищённое обновление 'price'
        """
        if price >= 0:
            self._price = price
        else:
            raise ValueError('must be >= 0')


if __name__ == '__main__':
    ad_1 = {
        "title": "iPhone X",
        "price": 100,
        "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
        }
    }

    ad_2 = {
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
            "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }

    # примеры работы кода:
    advert_2 = Advert(ad_2)
    print(advert_2.__dict__)
    print(advert_2.location.address)
    print(advert_2.price)
    advert_2.price = 100
    print(advert_2.price)
    print(advert_2.__dict__)

    lesson_str = """{
    "title": "python",
    "price": 0,
    "location": {
    "address": "город Москва, Лесная, 7",
    "metro_stations": ["Белорусская"]
    }
    }"""
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    # обращаемся к атрибуту location.address
    print(lesson_ad.location.address)

    dog_str = """{
    "title": "Вельш-корги",
    "price": 1000,
    "class": "dogs"
    }"""
    dog = json.loads(dog_str)
    dog_ad = Advert(dog)
    # обращаемся к атрибуту `dog_ad.class_` вместо `dog_ad.class`
    print(dog_ad.class_)

    # пытаемся сделать объявление с отрицательной ценой - ошибка
    lesson_str = '{"title": "python", "price": -1}'
    lesson = json.loads(lesson_str)
    try:
        lesson_ad = Advert(lesson)
    except ValueError as e:
        print(e)

    # пытаемся заменить цену на отрицательную - ошибка
    lesson_str = '{"title": "python", "price": 1}'
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    try:
        lesson_ad.price = -3
    except ValueError as e:
        print(e)

    # в случае отстувия поля price в JSON-объекте возвращает 0
    lesson_str = '{"title": "python"}'
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    lesson_ad.price

    # при отсутствии атрибута `title` - ошибка
    laptop_str = '{"price": 100000, "location": {"address":\
     "город Москва, Лесная, 7", "metro_stations": ["Белорусская"]}}'
    laptop = json.loads(laptop_str)
    try:
        laptop_ad = Advert(lesson)
    except ValueError as e:
        print(e)
