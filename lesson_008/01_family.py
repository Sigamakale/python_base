# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint


######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:
    # TODO Атрибуты класса необходимо использовать только если нужно сохранить
    # TODO какую-то общую информацию для всех классов. В данном случае
    # TODO citizen правильней сделать атрибутом экземпляра класса.
    citizen = 0

    def __init__(self):
        self.money = 100
        self.eat = 50
        self.mud = 0

    def __str__(self):
        return 'В доме жителей {}, еды {}, денег {}, грязи {}'.format(self.citizen, self.eat, self.money, self.mud)


class Human:
    # TODO Атрибуты класса необходимо использовать только если нужно сохранить
    # TODO какую-то общую информацию для всех классов. В данном случае
    # TODO is_live правильней сделать атрибутом экземпляра класса. Ведь гибель
    # TODO одночего человека не должна вести к смерти всех остальных.
    is_live = True
    # TODO Все люди могут потреблять различное колличество еды, по этому
    # TODO total_eating необходимо сделать атрибутом экземпляра класса.
    total_eating = 0

    def __init__(self, name, house, color):
        self.name = name
        self.house = house
        self.fullness = 30
        self.happyness = 100
        self.color = color
        house.citizen += 1

    def __str__(self):
        if self.is_live:
            return '{}, сытость {}, счастье {}'.format(self.name, self.fullness, self.happyness)
        else:
            return '{} умер(ла)'.format(self.name)

    def act(self):
        if self.fullness < 30 and self.house.eat > 0:
            self.eat()

    def eat(self):
        need_food = 30 - self.fullness
        need_food = need_food if self.house.eat > need_food else self.house.eat
        self.fullness += need_food
        self.house.eat -= need_food
        self.total_eating += need_food
        cprint('{} покушал, всего съедено {}'.format(self.name, self.total_eating), color=self.color)


class Husband(Human):
    # TODO Атрибуты класса необходимо использовать только если нужно сохранить
    # TODO какую-то общую информацию для всех классов. В данном случае
    # TODO total_money правильней сделать атрибутом экземпляра класса
    total_money = 0

    def __init__(self, name, house, color):
        super().__init__(name=name, house=house, color=color)
        self.color = color

    def __str__(self):
        return super().__str__() + ', всего заработано {}'.format(self.total_money)

    def act(self):

        if self.is_live:
            dice = randint(1, 2)
            if self.house.mud >= 90:
                self.happyness -= 10
            if self.fullness < 0 or self.happyness < 10:
                self.is_live = False
                cprint('{} не выжила'.format(self.name), color='red')
            elif self.fullness < 30 and self.house.eat > 0:
                super().act()
            elif self.house.money == 0:
                self.work()
            elif dice == 1:
                self.work()
            elif dice == 2:
                self.gaming()

    def work(self):
        self.fullness -= 10
        self.house.money += 150
        self.total_money += 150
        cprint('{} сходил на работу'.format(self.name), color=self.color)

    def gaming(self):
        self.fullness -= 10
        self.happyness += 20
        cprint('{} поиграл'.format(self.name), color=self.color)


class Wife(Human):
    # TODO Атрибуты класса необходимо использовать только если нужно сохранить
    # TODO какую-то общую информацию для всех классов. В данном случае
    # TODO fur_coat_count правильней сделать атрибутом экземпляра класса
    fur_coat_count = 0

    def __init__(self, name, house, color):
        super().__init__(name=name, house=house, color=color)
        self.color = color

    def __str__(self):
        return super().__str__() + ', кол-во шуб {}'.format(self.fur_coat_count)

    def act(self):

        if self.is_live:
            if self.house.mud >= 90:
                self.happyness -= 10
            if self.fullness < 0 or self.happyness < 10:
                self.is_live = False
                cprint('{} не выжила'.format(self.name), color='red')
            elif self.fullness < 30 and self.house.eat > 0:
                super().act()
            elif self.house.money >= 350 + 30 * self.house.citizen:
                self.buy_fur_coat()
            elif self.house.mud >= 100:
                self.clean_house()
            else:
                self.shopping()

    def shopping(self):
        self.fullness -= 10
        money_need = 30 * self.house.citizen - self.house.eat
        if self.house.money >= money_need:
            self.house.eat += money_need
            self.house.money -= money_need
            cprint('{} купила еды'.format(self.name), color=self.color)
        elif self.house.money <= money_need:
            self.house.eat += self.house.money
            self.house.money -= self.house.money
            cprint('{} купила еды на последние деньги'.format(self.name), color=self.color)

    def buy_fur_coat(self):
        self.fullness -= 10
        self.house.money -= 350
        self.happyness += 60
        self.fur_coat_count += 1
        cprint('{} купила шубу'.format(self.name), color=self.color)

    def clean_house(self):
        self.fullness -= 10
        self.house.mud -= 100
        cprint('{} прибралась'.format(self.name), color=self.color)


home = House()
serge = Husband(name='Сережа', house=home, color='cyan')
masha = Wife(name='Маша', house=home, color='magenta')

print(serge)
print(masha)
print(home)

for day in range(365):
    cprint('================== День {} =================='.format(day + 1), color='red')
    serge.act()
    masha.act()
    home.mud += 5
    cprint(serge, color='white')
    cprint(masha, color='white')
    cprint(home, color='white')

print('\n Итого за год:')
print('  1) заработано:', serge.total_money, ';')
print('  2) куплено шуб:', masha.fur_coat_count, ';')
print('  3) {} съел:'.format(serge.name), serge.total_eating, ';')
print('  4) {} съела:'.format(masha.name), masha.total_eating, ';')

######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов

#
# class Cat:
#
#     def __init__(self):
#         pass
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass
#
#     def soil(self):
#         pass
#
#
# ######################################################## Часть вторая бис
# #
# # После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
# #
# # Ребенок может:
# #   есть,
# #   спать,
# #
# # отличия от взрослых - кушает максимум 10 единиц еды,
# # степень счастья  - не меняется, всегда ==100 ;)
#
# class Child:
#
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return super().__str__()
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass
#
#
# # TODO после реализации второй части - отдать на проверку учителем две ветки
#
#
# ######################################################## Часть третья
# #
# # после подтверждения учителем второй части (обоих веток)
# # влить в мастер все коммиты из ветки develop и разрешить все конфликты
# # отправить на проверку учителем.
#
#
# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')
#

# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')