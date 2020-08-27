# -*- coding:utf-8 -*-
# /usr/bin/python3
# this script will defined the model of doloc town's person or corporation

class Occupations:

    FARMER = 0
    COOK = 1

class Occupation:
    ''' describe the status of one person's '''

    def __init__(self,_type):

        self._type = _type
        self.level = 0          # you can more easily get target job when you has a large level
        

class Slot:
    '''describe the groud of this world, you can build different constructor
    on this slot'''

    def __init__(self):

        pass

class __person:
    '''person is a base class contained some basic properties'''

    def __init__(self,name):

        self.name = name
        self.hungry_value = 100
        self.thirsty_value = 100
        self.money = 0