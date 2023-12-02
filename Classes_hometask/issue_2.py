import keyword
import json


class ColorizeMixin:
    def __repr__(self):
        color_option = '\033[' + str(self.repr_color_code) + 'm{}'
        s = f'{self.title} | {self.price} ₽'
        return color_option .format(s)


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


class Advert(ColorizeMixin, Dict2Obj):
    """
    Динамически создаёт атрибуты экземпляра класса из атрибутов JSON-объекта.
    Отличается от класса Dict2Obj тем, что имеет свойство price:
    проверяет, что значение не отрицательное и при создании объекта и при
    присваивании
    """
    repr_color_code = 33  # yellow

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
        # raise AttributeError('Изменение цены невозможно')
        if price >= 0:
            self._price = price
        else:
            raise ValueError('must be >= 0')

    def __repr__(self):
        color_option = '\033[' + str(self.repr_color_code) + 'm{}'
        s = f'{self.title} | {self.price} ₽'
        return color_option .format(s)


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

    advert_2 = Advert(ad_2)
    print(advert_2)
