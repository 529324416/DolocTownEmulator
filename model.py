# -*- coding:utf-8 -*-
# /usr/bin/python3
# this script will defined the model of doloc town's person or corporation

from tools import *
from utils import *
import time
import random

class PropertyID:
    ''' the basic properties of each person '''

    hungry = 0
    thirsty = 1
    energy = 2
    energy_ex = 3

PropertyIDLabels = ["hungry","thirsty","energy","energy_ex"]

class DebufID:
    '''something need to be fixed'''

    HUNGRY = 0
    THIRSTY = 1
    TIRED = 2
    TIRED_EX = 3

DebufIDThresholds = [15,20,15,15]

class Properties:
    ''' set properties as a component of one person'''

    def __init__(self,host):
        ''' the host is the person who would own these informations'''

        self.host = host
        self.debufs = list()
        self.values = [100] * 4
        self.length = len(self.values)

    def __len__(self):

        return self.length

    def __getitem__(self,idx):

        return self.values[idx]

    def increase(self,property_id:int,value:int):
        ''' increase the property value of target host'''

        self.values[property_id] += value
        if property_id in self.debufs and self.values[property_id] >= DebufIDThresholds[property_id]:
            self.debufs.remove(property_id)
        
    def decrease(self,property_id:int,value:int):
        ''' decrease the property value of target host'''

        self.values[property_id] -= value
        if property_id not in self.debufs and self.values[property_id] < DebufIDThresholds[property_id]:
            self.debufs.append(property_id)

    def can_fixdebuf(self,debuf_id:int,stuff:Food):

        return self.values[debuf_id] + stuff.properties[debuf_id] >= DebufIDThresholds[debuf_id]
        
    def has_debuf(self,debuf_id):

        return debuf_id in self.debufs

class Person:
    '''person is a base class contained some basic properties'''

    def __init__(self,name):

        self.name = name
        self.properties = Properties(self)
        self.money = 0
        self.packet = list()
        self.pos = 'work_position'

        self.work_status = 0
        self.work_times = 0
        # pos can be work_position, 

    def can_afford_stuff(self,stuff:Food):

        return self.money >= stuff.value

    def find_best_food(self):

        tmp = findmax(self.packet,self.total_value_compute)
        if tmp != None:self.packet.remove(tmp)
        return tmp
    
    def total_value_compute(self,stuff):

        total = self.compute_eating_value(stuff)
        for idx in range(len(self.properties)):
            if self.properties.has_debuf(idx):
                if self.properties.can_fixdebuf(idx,stuff):
                    total += 1
        return total

    def compute_eating_value(self,stuff:Food)->float:
        ''' compute how much value does target food be taked'''

        total = 0
        for idx in range(len(self.properties)):
            total += min(100 - self.properties[idx],stuff.properties[idx])
        return total/stuff.total_value()

    def consume_stuff(self,stuff:Food):

        print("{} eating the food:{}".format(self.name,stuff))
        for idx in range(len(self.properties)):
            print("{}'s {} has increase {} points".format(self.name,PropertyIDLabels[idx],stuff.properties[idx]))
            self.properties.increase(idx,stuff.properties[idx])

    def work(self):

        self.work_times += 1
        self.work_status += round(random.random()/4,2)
        self.work_status = min(1.0,self.work_status)

        hv = random.randint(4,7)
        dv = random.randint(3,6)
        ev = random.randint(2,4)
        print("{} is working now,lost {} point food value，{} points drink value, {} points energy value".format(self.name,hv,dv,ev))
        print("{}'s current work status is {}%".format(self.name,self.work_status * 100))
        self.properties.decrease(PropertyID.hungry,hv)
        self.properties.decrease(PropertyID.thirsty,dv)
        self.properties.decrease(PropertyID.energy,ev)

        if self.work_status == 1.0:
            self.get_salary()

    def get_salary(self):

        salary = ((1/self.work_times)/0.125) * 100
        print(f"{self.name}'s work has done. and he has got {salary} money")
        self.work_times = 0
        self.work_status = 0

    def check_properties(self):
        '''检查机体是否处于待修复状态'''

        return len(self.properties.debufs) > 0

    def rest_for_moment(self):
        '''让机体冷却一段时间'''

        value = random.randint(3,7)
        print(f'{self.name} is rest now, has increase {value} energy points and 1 energy_ex points')
        self.properties.increase(PropertyID.energy,value)
        self.properties.increase(PropertyID.energy_ex,1)

    def maintain_life(self,shop):
        '''修复机体受损的部分'''

        if len(self.packet) > 0:
            food = self.find_best_food()
            if food != None:
                self.consume_stuff(food)
            else:
                self.go_shopping(shop)
        else:
            self.go_shopping(shop)
    
    def go_shopping(self,shop):

        print(f'{self.name} has reach shop now')
        tmp = findmax_with_condition(shop.goods,self.compute_eating_value,self.shop_condition)
        if tmp is None:
            print(f'{self.name} buy nothing, for he has no money')

        else:
            if shop.sell_goods2person(tmp,self):
                self.maintain_life()
            else:
                self.rest_for_moment()
        
    def shop_condition(self,stuff:Food):

        return stuff.price <= self.money

    def show_status(self):

        print('current status :({},{},{},{})'.format(
            self.properties.values[0],
            self.properties.values[1],
            self.properties.values[2],
            self.properties.values[3]
        ))

    def entry(self,shop):

        if self.check_properties():
            self.maintain_life(shop)
        else:
            self.work()


class Shop:

    def __init__(self):

        self.money = 0
        self.goods = list()

    def fetch_goods(self):
        ''' get some foods in this shop, and this action'''

        self.goods.append(generate_bread())
        self.goods.append(generate_water())

    def sell_goods2person(self,stuff:Food,human:Person):

        self.goods.remove(stuff)
        if human.can_afford_stuff(stuff):
            human.money -= stuff.value
            human.packet.append(stuff)
            return True
        self.goods.append(stuff)
        return False

    def has_more(self,ID):

        return len(self.goods[ID]) > 0


class Game:

    def __init__(self):

        self.worker = Person("王子饼干")
        self.shop = Shop()

    def entry(self):

        while 1:
            self.worker.show_status()
            time.sleep(1)
            self.worker.entry(self.shop)

if __name__ == "__main__":
    
    game = Game()
    game.entry()