# -*- coding:utf-8 -*-
# /usr/bin/python3
# this script will defined the model of doloc town's person or corporation

from tools import *
from utils import *
import random


class Debuf:
    '''something need to be fixed'''

    HUNGRY = 0
    THIRSTY = 1
    TIRED = 2

class Person:
    '''person is a base class contained some basic properties'''

    def __init__(self,name):

        self.name = name
        self.hungry_value = 100
        self.thirsty_value = 100
        self.energy_value = 100
        self.energy_value_ex = 100
        self.money = 0

        self.packet = list()
        self.debuff = list()

        self.pos = [random.randint(1,10),random.randint(1,10)]

    def life_check(self):
        '''check if this person is in normal status'''

        if self.hungry_value < 15:
            self.debuff.append(Debuf.HUNGRY)
        if self.thirsty_value < 20:
            self.debuff.append(Debuf.THIRSTY)
        if self.energy_value < 20:
            self.debuff.append(Debuf.TIRED)

    def can_afford_stuff(self,stuff:Food):

        return self.money >= stuff.value

    def find_best_food(self):

        tmp = findmax(self.packet,self.total_value_compute)
        if tmp != None:self.packet.remove(tmp)
        return tmp
    
    def total_value_compute(self,stuff):

        total = self.compute_eating_value(stuff)
        if Debuf.HUNGRY in self.debuff:
            if self.can_fixhungry(stuff):
                total += 1
        
        if Debuf.THIRSTY in self.debuff:
            if self.can_fixthirsty(stuff):
                total += 1

        if Debuf.TIRED in self.debuff:
            if self.can_fixtired(stuff):
                total += 1

        return total

    def can_fixthirsty(self,stuff:Food):

        return stuff.drink + self.thirsty_value >= 20

    def can_fixhungry(self,stuff:Food):

        return stuff.food + self.hungry_value >= 15

    def can_fixtired(self,stuff:Food):

        return stuff.energy + self.energy_value >= 15

    def compute_eating_value(self,stuff:Food)->float:
        ''' compute how much value does target food be taked'''

        total = 0
        total += min(100 - self.thirsty_value,stuff.drink)
        total += min(100 - self.hungry_value,stuff.food)
        total += min(100 - self.energy_value,stuff.energy)
        total += min(100 - self.energy_value_ex,stuff.energy_ex)
        return total/stuff.total_value()

class Shop:

    def __init__(self):

        self.money = 0
        self.goods = dict(bread=list(),water=list())

    def fetch_goods(self):
        ''' get some foods in this shop, and this action'''

        self.goods['water'].append(generate_water())
        self.goods['bread'].append(generate_bread())

    def sell_goods2person(self,ID,human:Person):

        if self.has_more(ID):
            stuff = self.goods[ID].pop()
            if human.can_afford_stuff(stuff):
                human.money -= stuff.value
                human.packet.append(stuff)
                return True
        return False

    def has_more(self,ID):

        return len(self.goods[ID]) > 0


if __name__ == "__main__":
    
    p = Person("A")
    p.thirsty_value = 10
    p.hungry_value = 10
    p.energy_value = 50

    p.packet.append(generate_water())
    p.packet.append(generate_bread())
    p.packet.append(generate_bread())

    p.life_check()
    print(p.find_best_food())
    print(p.packet)