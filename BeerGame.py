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
        if wholesaler_demand > 1.5 * self.inventory:
            return 3 * np.abs(self.inventory - wholesaler_demand)
        elif (wholesaler_demand <= 1.5 * self.inventory) and (wholesaler_demand >= self.inventory / 1.5):
            return wholesaler_demand
        else:
            return wholesaler_demand / 1.5
    
    
DELAY = 4
NUM_WEEKS = 24

class Environment:
    def __init__(self):
        
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
        
        self.a_store = Retailer(self.brewer_inventory[-1])
        self.a_wholesaler = Wholesaler(self.wholesaler_inventory[-1])
        self.a_brewer = Brewery(self.retailer_inventory[-1])
        
    def run_simulation(self):        
        for i in range(DELAY, NUM_WEEKS):
            self.customer_order.append(8)

            self.a_brewer.get_goods(self.brewer_order[i-DELAY])
            delivered_to_wholesaler = self.a_brewer.sell_goods(self.wholesaler_order[i-DELAY])
            
            self.a_wholesaler.get_goods(delivered_to_wholesaler)
            delivered_to_retailer = self.a_wholesaler.sell_goods(self.retailer_order[i-DELAY])
            
            self.a_store.get_goods(delivered_to_retailer)
            delivered_to_customer = self.a_store.sell_goods(self.customer_order[i])
            
            self.brewer_sold.append(delivered_to_wholesaler)
            self.wholesaler_sold.append(delivered_to_retailer)
            self.retailer_sold.append(delivered_to_customer)
            
            self.brewer_inventory.append(self.a_brewer.inventory)
            self.wholesaler_inventory.append(self.a_wholesaler.inventory)
            self.retailer_inventory.append(self.a_store.inventory)

            self.brewer_order.append(self.a_brewer.brew_beer(self.wholesaler_order[i]))
            self.wholesaler_order.append(self.a_wholesaler.create_order(self.retailer_order[i]))
            self.retailer_order.append(self.a_store.create_order(self.customer_order[i]))

a_env = Environment()
a_env.run_simulation()  

a_env.retailer_order
a_env.retailer_inventory

a_env.wholesaler_order
a_env.wholesaler_inventory

a_env.brewer_order
a_env.brewer_inventory

model_time = list(range(NUM_WEEKS))

plt.plot(model_time, a_env.retailer_order)
plt.plot(model_time, a_env.wholesaler_order)
plt.plot(model_time, a_env.brewer_order)

plt.plot(model_time, a_env.retailer_inventory)
plt.plot(model_time, a_env.wholesaler_inventory)
plt.plot(model_time, a_env.brewer_inventory)
