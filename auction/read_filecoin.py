#! /usr/bin/python3

import json
import multi_dutch
import math
import random
import time

def run_auction(data, n_bidders, stats, run):
    better = 0
    worse = 0

    Items = []
    reser_prices = {}
    Bidders = []
    valuations = {}


    miners = set()
    counter = 0
    for entry in data:
        #convert the price to USD for a GB for a month format (FC expresses the price in bytes per block (~30s))
        filecoin_price = float(entry['Price'])*1000000*86400
        converted_price = int(filecoin_price * 1000)
        if(filecoin_price != 0 and converted_price == 0):
            converted_price = 1
        #discard items with worse price than google
        if(converted_price <= 3600):
            better += 1
        else:
            worse += 1
            #continue

        id = "I"+str(counter)
        counter += 1

        converted_price -= (converted_price %1000)

        print("Miner:", entry['Miner'], "ID:", id, "reservation price:", converted_price)

        #check if the input file is correct
        if(entry['Miner'] in miners):
            print("The miners list is not unique!")
            quit()
        else:
            miners.add(id)

        Items.append(id)
        max_price = 4201
        reser_prices[id] = converted_price

    print("Detected", better, "better miners and", worse, "worse miners than google")


    #create biddersToItems
    for id in range(0, n_bidders):
        bidderID  = "B"+str(id)
        Bidders.append(bidderID)
        
        for itemID in Items:
            evaluation = random.randrange(3000, 4200)
            valuations[bidderID,itemID] = evaluation

    auction = multi_dutch.Auction(Items, reser_prices, Bidders, valuations, max_price)
    start = time.time()
    auction.solve()
    end = time.time()
    auction.print_assignments()
    net_avg, price_avg = auction.verify()


    print("Avg net valuation:", net_avg, "Avg price:", price_avg)
    stats['ratio'].append(n_bidders/better)
    stats['net_avg'].append(net_avg)
    stats['price_avg'].append(price_avg)
    stats['run'].append(run)
    stats['time'].append(end - start)

def main():
    json_file='../data/filecoin_miners.json'
    json_data = "["
    first = True
    with open(json_file, "r") as lines:
        array = []
        for line in lines:
            if(first):
                json_data += line
                first = False
            else:
                json_data += "," + line

    json_data += "]"
    data = json.loads(json_data)

    stats = {}
    stats['ratio'] = list()
    stats['net_avg'] = list()
    stats['price_avg'] = list()
    stats['run'] = list()
    stats['time'] = list()


    for run in range(0, 10):
        for i in range(1, 70):
            print("~~~~~~~~~~~~~~Running with", i , "bidders~~~~~~~~~~~~~~")
            run_auction(data, i, stats, run)
            

    print(stats)

if __name__=="__main__":
	main()
