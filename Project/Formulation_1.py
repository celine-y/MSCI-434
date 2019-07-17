#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 12:37:33 2019

@author: celine
"""

from gurobipy import *
import pandas as pd 
import numpy as np

# Reading in Data
rc_order = pd.read_csv('Data - order_rc 2.csv', index_col='Type A/Type K')
x_bar = pd.read_csv('Data - x_bar 2.csv', index_col='Type k').iloc[[12]].values[0]

k_a = rc_order.values
print(k_a)
# Containts
k = 17
a= 41
m = 12

# Create model
model = Model()

# Variables
n = model.addVars(m, k, vtype=GRB.INTEGER, name='n') #n_mk
x = model.addVars(k, vtype=GRB.INTEGER, name='x') #x_k
y = model.addVars(a, k, vtype=GRB.BINARY, name='y') #y_ak
z = model.addVars(k, vtype=GRB.BINARY, name='z') #z_k

# Objective Function
model.setObjective(quicksum(z[i] for i in range(0, k)), GRB.MINIMIZE)

# Constraints
# 1)
for i in range(0, a):
    model.addConstr(quicksum(k_a[i, j]*y[i, j] for j in range(0, k)) == 1)
    
# 2)
for i in range(0, k): #K
    for j in range(0, a): #A
        model.addConstr(z[i] >= y[j, i])
        
# 3)
for i in range(0, k): #k
    for j in range(0, m): #m
        model.addConstr(quicksum(k_a[h, i]*y[h, i] for h in range(0, a)) == n[j, i])
        #model.addConstr(quicksum(y[h, i] for h in range(0, a)) == n[j, i])
        

# 4)
for i in range(0, k): #k
    for j in range(0, m): #m
        model.addConstr(n[j, i] <= x[i])

# 5)
for i in range(0, k): #k
    model.addConstr(x[i] <= x_bar[i])

model.update()
model.optimize()

for g in model.getVars():
    if g.x > 0:
        print(g.varName, g.x)
