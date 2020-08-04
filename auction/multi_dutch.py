from random import randint,seed
import numpy as np
import Hungarian
import time
import json
import pandas as pd

#Item related DS
#Items      = []
#prices       = {}
#reser_prices = {}#reservation prices
#itemsToBidders         = {}
#Bidder related DS
#Bidders    = []
#demand_correspondence  = {}
#biddersToItems         = {}
#valuations = {}
#seedInput    = 1
#delta_price  = 1#delta price: has to be selected in a way that captures the bidders' valuation differences

class Auction:
	def __init__(self, items, reser_prices, bidders, valuations):
		self.Items = items
		self.reser_prices= reser_prices
		self.prices = {}
		self.itemsToBidders = {}
		for item in self.Items:
 			self.prices[item] = 101#price above any possible valuation
 			self.itemsToBidders[item]= None

		self.Bidders = bidders
		self.demand_correspondence = {}
		self.biddersToItems = {}
		for bidder in self.Bidders:
			self.demand_correspondence[bidder]  = []#the demand correspondence is empty
			self.biddersToItems[bidder]  = None

		self.valuations = valuations
		self.seedInput = 1
		self.delta_price = 1



	def solve(self):
		U = set()#set of universally allocated items
		setOfItems = set(self.Items)
		while True:#the maximum number of iterations is bounded by max_price/delta_p
			#=================================
			#collect the demand correspondence for each bidder
			#=================================
			demand_valuation = {}
			for bidderID in self.Bidders:
				#initialisation
				max_valuation  = 0.0
				self.demand_correspondence[bidderID] = []
				#find the set of items that maximise bidders valuation
				for itemID in self.Items:
					candidate_net_valuation  = self.valuations[bidderID,itemID] - self.prices[itemID]
					if candidate_net_valuation > max_valuation:
						self.demand_correspondence[bidderID] = []
						max_valuation  = candidate_net_valuation
					if candidate_net_valuation == max_valuation:
						self.demand_correspondence[bidderID].append(itemID)
				demand_valuation[bidderID]  = max_valuation
			#=================================
			#estimate the set of universally allocated items
			U  = self.universally_allocated_items(demand_valuation)
			#=================================
			if setOfItems == U:
				break
			for itemID in setOfItems - U:
				self.prices[itemID] = max(self.prices[itemID] - self.delta_price, self.reser_prices[itemID])
				#print("reducing price of", itemID,  self.prices[itemID], self.delta_price)

	def universally_allocated_items(self, demand_valuation):
		#=================================
		#calculate provisional allocation -> apply the hungarian method -> complexity O(n^3)
		#=================================
		#initialisation:
		for bidderID in self.Bidders:
			self.biddersToItems[bidderID]  = None
		for itemID in self.Items:
			self.itemsToBidders[itemID]    = None
		#create cost of bipartite graph
		cost_list = []#The cost matrix of the bipartite graph: array
		for bidderID in self.Bidders:
			cost_of_bidder = []
			for itemID in self.Items:
				if itemID in self.demand_correspondence[bidderID]:
					cost_of_bidder.append(-demand_valuation[bidderID])#The hungarian method solves a minimisation problem
				else:
					cost_of_bidder.append(1.0)
			cost_list.append(cost_of_bidder)
		cost  = np.array(cost_list)
		row_ind, col_ind = Hungarian.linear_sum_assignment(cost)#returens an array of row indices and one of corresponding column indices giving the optimal assignment
		for index in range(len(row_ind)):
			bidderID  = self.Bidders[row_ind[index]]
			itemID    = self.Items[col_ind[index]]
			if itemID in self.demand_correspondence[bidderID]:
				self.biddersToItems[bidderID]  = itemID
				self.itemsToBidders[itemID]    = bidderID
		#=================================
		#find universally allocated items -> O(n^3)
		#=================================
		#Step 0: initial set of universally allocated items U
		U  = set()
		A  = set()#set of items with price equal to their reservation price
		
		for itemID in self.Items:#if an item has reached its reservation price
			if self.prices[itemID] == self.reser_prices[itemID]:
				U.add(itemID)
				A.add(itemID)
		for bidderID in self.Bidders:#or if bidder is assigned to null item while there are items in her demand correspondence
			if self.biddersToItems[bidderID]==None:
				for itemID in self.demand_correspondence[bidderID]:
					if itemID not in U:
						U.add(itemID)
		#calculate the set of universally allocated items
		for index in range(len(self.Items)):#up to n iterations
			#Step 1: find the set of bidders assigned to items in U, T
			T = set()
			for itemID in U:
				if self.itemsToBidders[itemID]==None:
					continue
				T.add(self.itemsToBidders[itemID])
			#Step 2: find the set of provisionally allocated items requested by T at a price higher thant their reservation, W
			W = set()
			for bidderID in T:
				for itemID in self.demand_correspondence[bidderID]:
					if self.prices[itemID] > self.reser_prices[itemID]:
						W.add(itemID)
			#Step 3a:if W subset of U return U and items with price equal to their reservation
			if W.issubset(U):
				return U.union(A)
			#Step 3b:else increment the set of universally allocated items
			U = U.union(W)
		return U

	def print_assignments(self):
		print("Items", self.Items)
		print("Bidders", self.Bidders)
		for bidderID in self.Bidders:
			itemID  = self.biddersToItems[bidderID]
			if itemID != None:
				print("Bidder ", bidderID,", acquired item: ", itemID,", at price: ", self.prices[itemID]," with net valuation: ", self.valuations[bidderID,itemID] - self.prices[itemID])
			else:
				print("Bidder ", bidderID, "acquired the null item")

	def verify(self):
		net_sum = 0
		price_sum = 0
		assigned_items = 0
		for bidderID in self.Bidders:
			my_itemID  = self.biddersToItems[bidderID]
			net_valuation = 0
			if(my_itemID != None):
				net_valuation = self.valuations[bidderID,my_itemID] - self.prices[my_itemID]
				price_sum += self.prices[my_itemID]
				assigned_items += 1
			net_sum += net_valuation


			for itemID in self.Items:
				other_valuation = self.valuations[bidderID,itemID] - self.prices[itemID]
				#had to add delta price to cover for computation inaccuracy with floats
				if( (net_valuation + self.delta_price) < other_valuation):
					print("Users", bidderID, "would be better with item", itemID, "with net evaluation", other_valuation)
					return

		print("Assignment verified correctly")

		return (net_sum/len(self.Bidders), price_sum/assigned_items)


def main():
	item1ID = "item1"
	item2ID = "item2"
	item3ID = "item3"
	Items = []
	Items.append(item1ID)
	Items.append(item2ID)
	Items.append(item3ID)
 	
	reser_prices = {}
	reser_prices[item1ID]  = 1
	reser_prices[item2ID]  = 1
	reser_prices[item3ID]  = 1
	bidder1ID = "b1"
	bidder2ID = "b2"
	bidder3ID = "b3"
	bidder4ID = "b4"
	bidder5ID = "b5"
	Bidders = []
	Bidders.append(bidder1ID)
	Bidders.append(bidder2ID)
	Bidders.append(bidder3ID)
	Bidders.append(bidder4ID)
	Bidders.append(bidder5ID)


	valuations = {}
	valuations['b1','item1'] = 0
	valuations['b1','item2'] = 0
	valuations['b1','item3'] = 40

	valuations['b2','item1'] = 0
	valuations['b2','item2'] = 20
	valuations['b2','item3'] = 20

	valuations['b3','item1'] = 0
	valuations['b3','item2'] = 15
	valuations['b3','item3'] = 15

	valuations['b4','item1'] = 5
	valuations['b4','item2'] = 10
	valuations['b4','item3'] = 30

	valuations['b5','item1'] = 10
	valuations['b5','item2'] = 13
	valuations['b5','item3'] = 15

	auction = Auction(Items, reser_prices, Bidders, valuations)
	auction.solve()
	auction.print_assignments()
	auction.verify()

if __name__=="__main__":
	main()





	# results = {}
	# results['n'] = list()
	# results['auction'] = list()
	# results['verification'] = list()
	# results['total'] = list()
	# results['run'] = list()
	# results['gas_per_user'] = list()

	# #init()
	# simpleAuction()
	# auction()
	# print_assignments()
	# verify_assignment()
	# quit()
	# for run in range (1, 5, 1): 
	# 	for n in range (1, 10002, 500):
	# 		print(n)
	# 		init()
	# 		returnDummyAuction(number_of_bidders = n, number_of_items = 100)
	# 		#simpleAuction()

	# 		start = time.time()
	# 		auction()
	# 		end = time.time()

	# 		#print_assignments()

	# 		vstart = time.time()
	# 		#verify_assignment()
	# 		auction()
	# 		vend = time.time()

	# 		print("Time", end - start)
	# 		results['n'].append(n)
	# 		results['auction'].append(end - start)
	# 		results['verification'].append(vend - vstart)
	# 		results['total'].append((vend - vstart) + (end - start))
	# 		results['run'].append(run)
	# 		results['gas_per_user'].append(492048 + n*508)

	
	# df = pd.DataFrame(results)
	# print(df)
	# with open('test.txt', 'w') as file:
	# 	file.write(json.dumps(results))


# def simpleAuction():
# 	item1ID = "item1"
# 	item2ID = "item2"
# 	item3ID = "item3"
# 	Items.append(item1ID)
# 	Items.append(item2ID)
# 	Items.append(item3ID)
# 	for item in Items:
# 		prices[item]        = 101#price above any possible valuation
# 		itemsToBidders[item]= None

# 	reser_prices[item1ID]  = 1
# 	reser_prices[item2ID]  = 1
# 	reser_prices[item3ID]  = 1
# 	bidder1ID = "b1"
# 	bidder2ID = "b2"
# 	bidder3ID = "b3"
# 	bidder4ID = "b4"
# 	bidder5ID = "b5"
# 	Bidders.append(bidder1ID)
# 	Bidders.append(bidder2ID)
# 	Bidders.append(bidder3ID)
# 	Bidders.append(bidder4ID)
# 	Bidders.append(bidder5ID)
# 	for bidder in Bidders:
# 		demand_correspondence[bidder]  = []#the demand correspondence is empty
# 		biddersToItems[bidder]  = None

# 	valuations['b1','item1'] = 0
# 	valuations['b1','item2'] = 0
# 	valuations['b1','item3'] = 40

# 	valuations['b2','item1'] = 0
# 	valuations['b2','item2'] = 20
# 	valuations['b2','item3'] = 20

# 	valuations['b3','item1'] = 0
# 	valuations['b3','item2'] = 15
# 	valuations['b3','item3'] = 15

# 	valuations['b4','item1'] = 5
# 	valuations['b4','item2'] = 10
# 	valuations['b4','item3'] = 30

# 	valuations['b5','item1'] = 10
# 	valuations['b5','item2'] = 13
# 	valuations['b5','item3'] = 15



# def returnDummyAuction(number_of_bidders=15,number_of_items=30):
# 	"""
# 	initialises the set of bidders and items
# 	bidders' valuations for items take values between 1 and 100
# 	items' reservation prices take values from 1 to 50
# 	"""
# 	seed(seedInput)
# 	#create items' ID
# 	for item in range(1,number_of_items+1):
# 		itemID  = "I"+str(item)
# 		Items.append(itemID)
# 		prices[itemID]        = 101.0#price above any possible valuation
# 		reser_prices[itemID]  = float(randint(1,50))
# 		itemsToBidders[itemID]= None
# 	#create bidders' ID
# 	for bidder in range(1,number_of_bidders+1):
# 		bidderID  = "B"+str(bidder)
# 		Bidders.append(bidderID)
# 		demand_correspondence[bidderID]  = []#the demand correspondence is empty
# 		biddersToItems[bidderID]  = None
# 		for itemID in Items:
# 			valuations[bidderID,itemID] = float(randint(1,100))