# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 20:28:01 2019

@author: Konrad
"""
import numpy as np
import matplotlib.pyplot as plt

class Business:
    def __init__(self, inventory):
        self.inventory = inventory
        self.sold_goods = None
        
    def get_goods(self, supplied):
        self.inventory += supplied
    
    def sell_goods(self, demand):
        if demand >= self.inventory:
            self.sold_goods = self.inventory
            self.inventory = 0
        else:
            self.sold_goods = demand
            self.inventory -= demand
            
        return self.sold_goods

class Retailer(Business):
    def __init__(self, inventory):
        Business.__init__(self, inventory)
    
    def create_order(self, customer_demand):
        
        if customer_demand > 1.5 * self.inventory:
            return 3 * np.abs(self.inventory - customer_demand)
        elif (customer_demand <= 1.5 * self.inventory) and (customer_demand >= self.inventory / 1.5):
            return customer_demand
        else:
            return customer_demand / 1.5
            

class Wholesaler(Business):
    def __init__(self, inventory):
        Business.__init__(self, inventory)
        
    def create_order(self, retail_demand):
        if retail_demand > 1.5 * self.inventory:
            return 3 * np.abs(self.inventory - retail_demand)
        elif (retail_demand <= 1.5 * self.inventory) and (retail_demand >= self.inventory / 1.5):
            return retail_demand
        else:
            return retail_demand / 1.5

class Brewery(Business):
    def __init__(self, inventory):
        Business.__init__(self, inventory)
    
    def brew_beer(self, wholesaler_demand):
        pass

DELAY = 4
NUM_WEEKS = 24

class Environment:
    def __init__(self):
        self.a_store = Retailer(12)
        self.a_wholesaler = Wholesaler(12)
        self.a_brewer = Brewery(12)
                 
    def run_step(self):
        self.brewer_inventory = [12, 12, 12, 12]
        self.wholesaler_inventory = [12, 12, 12, 12]
        self.retailer_inventory = [12, 12, 12, 12]

        self.wholesaler_order = [4, 4, 4, 4]
        self.retailer_order = [4, 4, 4, 4]
        self.customer_order = [4, 4, 4, 4]
        self.brewer_order = [4, 4, 4, 4]
        
        self.retailer_sold = [4, 4, 4, 4]
        self.wholesaler_sold = [4, 4, 4, 4]
        self.brewer_sold = [4, 4, 4, 4]
        
        for i in range(DELAY, NUM_WEEKS):
            self.customer_order.append(8)
            print(i)

            self.a_brewer.get_goods(self.wholesaler_order[i])
            delivered_to_wholesaler = self.a_brewer.sell_goods(self.wholesaler_order[i-DELAY])
            
            self.a_wholesaler.get_goods(delivered_to_wholesaler)
            delivered_to_retailer = self.a_wholesaler.sell_goods(self.retailer_order[i-DELAY])
            
            self.a_store.get_goods(delivered_to_retailer)
            delivered_to_customer = self.a_store.sell_goods(self.customer_order[i])
            
            self.wholesaler_sold.append(delivered_to_retailer)
            self.brewer_sold.append(delivered_to_wholesaler)
            self.retailer_sold.append(delivered_to_customer)
            
            self.wholesaler_inventory.append(self.a_wholesaler.inventory)
            self.retailer_inventory.append(self.a_store.inventory)
            self.brewer_inventory.append(self.a_brewer.inventory)

            self.retailer_order.append(self.a_store.create_order(self.customer_order[i]))
            self.wholesaler_order.append(self.a_wholesaler.create_order(self.retailer_order[i]))
            self.brewer_order.append(self.a_brewer.brew_beer(self.wholesaler_order[i]))

a_env = Environment()
a_env.run_step()  

a_env.retailer_order
a_env.retailer_inventory

a_env.wholesaler_order
a_env.wholesaler_inventory


plt.plot(list(range(NUM_WEEKS)), a_env.retailer_order)
plt.plot(list(range(NUM_WEEKS)), a_env.wholesaler_order)
plt.plot(list(range()))

#steady_state = np.repeat(4, DELAY)
#week_1 = np.array([4])
#remaining_weeks = np.repeat(8, NUM_WEEKS - 1)
#
#customer_demand = np.concatenate((steady_state, week_1, remaining_weeks))