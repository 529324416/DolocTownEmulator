# -*- coding:utf-8 -*-
# !/usr/bin/python3
# * script would provide some basic funciton for game compute or controller

def findmax(objs,compute):
    ''' find the max value in objs evaluated by compute function
    @objs: a value list
    @compute: a compute function used to compute the value of obj'''

    _max,_tmp = 0,None
    for idx in range(len(objs)):
        if (_value:=compute(objs[idx])) > _max:
            _max,_tmp = _value,objs[idx]
    return _tmp

def findmax_with_condition(objs,compute,condition):
    ''' find the max value in objs evaluated by compute function
    @objs: a value list
    @compute: a compute function to compute the value of target obj
    @condition: filter the invalid objects'''

    _max,_tmp = 0,None
    for idx in range(len(objs)):
        if (_value:=compute(objs[idx])) > _max and condition(objs[idx]):
            _max,_tmp = _value,objs[idx]
    return _tmp