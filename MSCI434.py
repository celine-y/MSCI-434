#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:55:27 2019

@author: US
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
h = wh_c['Cost'].values
p_h = p['Holding cost'].values
p_cap = p['Capacity'].values
demand = cust['Demand'].values

m = Model()
n = len(d)

#variables
y = m.addVars(22, 22, vtype=GRB.INTEGER)
x = m.addVars(22, 22, vtype=GRB.INTEGER)
z = m.addVars(22, 1, vtype=GRB.BINARY)

# Objective Function
m.setObjective(
        0.187*quicksum(quicksum(t[j,k]*y[j,k] for j in range(22)) for k in range(22)) +
        quicksum(h[j]*z[j, 0] for j in range(22)) +
        0.187*quicksum(quicksum(p_h[i]*x[i,j] for i in range(22)) for j in range(22)) + 288 + 476
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

m.update()
m.optimize()
print('Min Distance', m.objVal)

for i in range(n):
    for j in range(n):
        if x[i,j].x >0 :
            print(i+1, '->', j+1 , ':', x[i,j].x)

"""
dij= np.asarray([[10000, 120, 220, 150, 210],
                 [120,10000, 100, 110, 130],
                 [220, 80, 10000, 160, 185],
                 [150, 10000,160, 10000, 190 ],
                 [210, 130, 185, 10000, 10000]
                 ])

m= Model()
n=len(dij)

#create variable
x= m.addVars(n,n, vtype= GRB.BINARY)
u= m.addVars(n-1, lb=2, vtype=GRB.INTEGER)

#Objective function
m.setObjective(quicksum(quicksum(dij[i,j]*x[i,j] for i in range(n)) for j in range(n)), GRB.MINIMIZE)

#Constraints

for i in range(n):
    m.addConstr(quicksum(x[i,j] for j in range(n)) == 1)

for j in range(n):
    m.addConstr(quicksum(x[i,j] for i in range(n)) == 1)

for i in range(n-1):
    for j in range(n-1):
        m.addConstr(u[i]-u[j] + n*x[i,j] <= n-1)

m.update()
m.optimize()

#print Output

print('Min Distance', m.objVal)


for i in range(n):
    for j in range(n):
        if x[i,j].x >0 :
            print(i+1, '->', j+1 , ':', x[i,j].x)

for i in range(n-1):
    print('u', i+2, '=', u[i].x)
"""
            