#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint


class Hero(object):
    """ Класс героя, который описывает поведение героя  """
    bot_move = 0
    hp = 100
    common_damage = (10, 20)
    strong_damage = (5, 25)
    hil_point = (10, 20)
    low_bot_hp = False

    def __init__(self, name='bot'):
        """ Инициализирует героя

         Args:
              name(str): имя героя
        """
        self.name = name

    def loos_hp(self, value):
        """Декрементирует значение self.hp на значение value, если self.hp < 0
        устанавливает в 0

        Args:
            value(int): значение нанесенного урона
        """
        self.hp -= value
        if self.hp <= 0:
            self.hp = 0

    def hil_hp(self, value):
        """Инкрементирует значение self.hp на значение value, если self.hp < 100
        устанвливает в 100

        Args:
            value(int): значение исцеления
        """
        if self.hp + value > 100:
            self.hp = 100
        else:
            self.hp += value

    def common_attack(self, hero):
        '''Вычисляет значение обычной атаки, отнимает значение от self.hp hero
        отображает в консоль действие и значение

        Args:
            hero(Hero): герой у которого вызвается метод loos_hp
        '''
        damage = randint(*self.common_damage)
        hero.loos_hp(damage)
        self.print_action('Обычный удар', damage)

    def strong_attack(self, hero):
        '''Вычисляет значение сильной атаки, отнимает значение от self.hp hero
        отображает в консоль действие и значение

        Args:
            hero(Hero): герой у которого вызвается метод loos_hp
        '''
        damage = randint(*self.strong_damage)
        hero.loos_hp(damage)
        self.print_action('Сильный удар', damage)

    def hill(self, hero):
        '''Вычисляет значение исцеления, прибавляет значение к self.hp у hero
        выводит в консоль действие и значение.

        Args:
            hero(Hero): герой у которого вызвается метод loos_hp
        '''
        point = randint(*self.hil_point)
        hero.hil_hp(point)
        self.print_action('Исцеление', point)

    def set_low_bot_hp(self):
        '''Устанавливает значение self.low_bot_hp в True, если self.hp <= 35 и наоборот '''
        if self.hp <= 35:
            self.low_bot_hp = True
        else:
            self.low_bot_hp = False

    def print_action(self, action, action_value):
        ''' Выводит в консоль действие и его значение '''
        print('Выполняет действие - {}({})'.format(action, action_value))


class Game(object):
    ''' Класс игры, который описывает поведение игры '''
    def create_hero(self, name=None):
        ''' Инициализирует игроков.
        Создает двух геровев: бота и игрока с именем :param name.

        Args:
            name(str): имя героя
        '''
        if name:
            return Hero(name)
        return Hero()

    def action_selection(self, hero):
        ''' Выбирает действие.
        Описывает поведение действия и его вероятности для :hero.

        Args:
            hero(Hero): герой у которого производится выбор действия
        '''
        actions = {'common_attack': randint(0, 100), 'strong_attack': randint(0, 100)}

        if hero.hp < 100:
            actions['hill'] = randint(0, 100)
        if hero.name == 'bot':
            hero.set_low_bot_hp()
            if hero.low_bot_hp:
                actions['hill'] += 20

        return max(actions, key=actions.get)

    def validate(self, value):
        ''' Производит валидацию.

        Args:
            value(str): введенное пользователем имя героя.

        :return: value если прошла валидация, если нет None
        '''
        if len(value) <= 0:
            print('хотя бы один символ')
        elif len(value) > 15:
            print('не больше пятнадцати символов')
        elif not isinstance(value,str):
            print('значение должно быть строкой')
        else:
            return value
        return None

    def step(self, hero_is_move, another_hero):
        '''Выполняет действие над героем.

        Args:
            hero_is_move(Hero): экземпляр класса Hero, игрок который ходит
            another_hero(Hero): экземпляр класса Hero, противник игрока
        '''
        action = self.action_selection(hero_is_move)
        if action == 'hill':
            getattr(hero_is_move, action)(hero_is_move)
        else:
            getattr(hero_is_move, action)(another_hero)

    def start(self):
        ''' Функция игры, запускает игру.
        Инициализирует игроков, определяет ход игрока, вызывает методы действия на игроков,
        инвертирует ход, отображает в консоль self.hp игроков, если self.hp < 0, отображает
        победителя.
         '''
        name = None
        while not name:
            name = self.validate(input('Введите имя(максимум 15 символов): '))
        player = self.create_hero(name)
        bot = self.create_hero()
        self.bot_move = randint(0, 1)
        while (player.hp and bot.hp) > 0:
            print('Ходит {}:'.format(bot.name if self.bot_move else player.name))
            if self.bot_move:
                self.step(bot, player)
            else:
                self.step(player, bot)
            print("Здоровье '{}':{} \nЗдоровье 'Компьютора':{}\n..........................".format(player.name,
                                                                                                   player.hp,
                                                                                                   bot.hp))
            self.bot_move = not self.bot_move
        print("Победил - {}!".format(player.name if bot.hp <= 0 else "Компьютор"))


game = Game()
game.start()
