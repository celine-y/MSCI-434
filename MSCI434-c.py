#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 14:03:34 2019

@author: celine
"""

from gurobipy import *
import numpy as np
import pandas as pd

t = pd.read_csv('Distance Constraints - Distance.csv', index_col='City')
wh_c = pd.read_csv('Distance Constraints - Warehouses.csv')
p = pd.read_csv('Distance Constraints - Plant.csv')
cust = pd.read_csv('Distance Constraints - Customer Locations.csv')

t = t.values
w_cap = wh_c['Capacity'].values
h = wh_c['New Cost'].values
p_h = p['Holding cost'].values
p_cap = p['Capacity'].values
demand = cust['Demand'].values
b_w = wh_c['Carbon Emission (tonnes)'].values

m = Model()
n = len(t)

#variables
y = m.addVars(22, 22, vtype=GRB.INTEGER)
x = m.addVars(22, 22, vtype=GRB.INTEGER)
z = m.addVars(22, 1, vtype=GRB.BINARY)

# Objective Function
m.setObjective(
        1870*quicksum(quicksum(t[j,k]*y[j,k] for j in range(22)) for k in range(22)) +
        quicksum(h[j]*z[j, 0] for j in range(22)) +
        1870*quicksum(quicksum(p_h[i]*x[i,j] for i in range(22)) for j in range(22)) + 288 + 476
        , GRB.MINIMIZE)

#Constraints
for i in range(22):
    m.addConstr(quicksum(x[i,j] for j in range(22)) <= p_cap[i])
        
for j in range(22):
    m.addConstr(quicksum(y[j,k] for k in range(22)) <= w_cap[j])
    
for k in range(22):
    m.addConstr(quicksum(y[j,k] for j in range(22)) >= demand[k])
    
for j in range(22):
    m.addConstr(quicksum(x[i, j] for i in range(22)) == quicksum(y[j, k] for k in range(22)))
    
for j in range(22):
    m.addConstr(quicksum(y[j,k] for k in range(22)) <= 10000*z[j, 0])
    
for j in range(22):
    m.addConstr(quicksum(x[i,j] for i in range(22)) <= 10000*z[j, 0])
    
for j in range(22):
    m.addConstr(449+269 + b_w[j]*z[j, 0] <= 2500)
    
# z-values
    m.addConstr(quicksum(z[j, 0] for j in range(22)) <= 8)
    
# x-values
    m.addConstr(quicksum(x[0, j] for j in range(n)) >= 1)
    m.addConstr(quicksum(x[3, j] for j in range(n)) >= 1)

m.update()
m.optimize()
print('Min Distance', m.objVal)

print('X values --------------------------->')
for i in range(n):
    for j in range(n):
        if x[i,j].x >0 :
            print(i, '->', j , ':', x[i,j].x)
print('Y values ---------------------------->')
for i in range(n):
    for j in range(n):
        if y[i,j].x >0 :
            print(i, '->', j , ':', y[i,j].x)       
print('Z values --------------------------->')
            
for i in range(n):
    if (z[i,0].x > 0):
        print(i , ':', z[i,0].x)