# -*- coding:utf-8 -*-
# /usr/bin/python3
# provide different tools for citizen

class StuffType:

    CAN_BE_ATE = 0

class __stuff:
    ''' the base class of stuff, and those stuff would has different properties'''

    def __init__(self,_type):

        self.type = _type

class Food(__stuff):

    def __init__(self,name,value):

        super(Food,self).__init__(StuffType.CAN_BE_ATE)
        self.name = name
        self.value = value

    def initialize_properties(self,food,drink,energy,energy_ex):
        ''' the food can be used for life support'''

        self.food = food
        self.drink = drink
        self.energy = energy
        self.energy_ex = energy_ex

    def total_value(self):

        return self.food + self.drink + self.energy_ex + self.energy

    def __repr__(self):

        return f"<({self.name},${self.value}),({self.food},{self.drink},{self.energy},{self.energy_ex})>"

    @staticmethod
    def generate_food(name,value,food,drink,e,eex):

        _food = Food(name,value)
        _food.initialize_properties(food,drink,e,eex)
        return _food

def generate_water():
    '''generate a bottle of water, and this can help you to get some thirsy value
    with nothing bad'''

    return Food.generate_food("一瓶矿泉水",1.5,0,10,2,0)

def generate_bread():
    '''generate a bread, and bread can help you get some hungry value
    but it will decrease your thirsty value'''

    return Food.generate_food("一块面包",2.2,10,-1,5,0)