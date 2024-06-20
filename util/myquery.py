"""
    Module provides the myquery Class
"""
import requests
from .mycollection import mycollection
import time
class myquery:
    """
        Represents a scryfall query
    """
    def __init__(self,col,q,inverse = False):
        self.q = q
        self.collection = dict()
        self.response = None
        self.result_cards = []
        self.result_len = -1

        #load collection
        self.load_collection(col)
        #run query
        self.get()
        #filter by collection 
        if inverse:
            self.page_and_filter_inverse()
        else:
            self.page_and_filter()

        del self.collection
        card_names = set()
        for card in self.result_cards:
            card_names.add(card["name"])
        self.unique_collection_cards = len(card_names);
        del card_names

        ##request

        #self.q = q
        #rest are optional
        #self.unique = None
        #self.order = None
        #self.direction = None
        #self.include_extras = False
        #self.include_multilingual = False
        #self.include_variations = False
        #self.page = None
        #self.format = None
        #self.pretty = False

       
        ##response object error

        #self.object = None
        #self.code = None
        #self.details = None
        #self.status = None
        ##last 2 can be null or missing
        #self.warnings = None
        #self.type = None

        
        ##response object list

        #self.object = None
        #self.has_more = None
        #self.data = None
        ##last 3 can be null or missing
        #self.total_cards = None
        #self.next_page = None
        #self.warnings = None

    def load_collection(self,col):
        """Loads the collection as a lookup table by card name"""
        for card in col.cards:
            if card["name"] in self.collection:
                self.collection[card["name"]].append(card)
            else:
                self.collection[card["name"]] = [card]
    
    def get(self):
        """Runs the query and gets the initial results"""
        r = requests.get("https://api.scryfall.com/cards/search",params={"q":self.q})
        response = r.json()
        if response["object"] == "error":
            print("ERROR:error type "+str(r)+"\n"+str(response))
        elif response["object"] == "list":
            if "warnings" in response:
                print("WARNINGS:",response["warnings"])
            self.response = response
            self.result_len = response["total_cards"]
        else:
            print("ERROR:Unkown Response Object",r["object"])

    def page_and_filter_inverse(self):
        """Gathers results and filters them by our filter, as well as by not being in our collection"""
        results_counter = 0
        digits = len(str(self.result_len))
        print("Filtering:{}/{}".format(str(results_counter).zfill(digits),self.result_len),end="\r")
        while True:
            if not self.response:
                return
            for card in self.response["data"]:
                results_counter += 1
                if card["name"] not in self.collection:
                    #TODO might need to fudge the MTGD_... values in case i assume they exist anywhere beyond here
                    card["MTGD_foil_count"] = 0
                    card["MTGD_nonfoil_count"] = 0
                    self.result_cards.append(card)
            print("Filtering:{}/{}".format(str(results_counter).zfill(digits),self.result_len),end="\r")
            if not self.response["has_more"]:
                print()
                break
            else: 
                time.sleep(.2)
                self.response = requests.get(self.response["next_page"]).json()

    def page_and_filter(self):
        """Gathers results and filters them by our filter, as well as being in our collection"""
        results_counter = 0
        digits = len(str(self.result_len))
        print("Filtering:{}/{}".format(str(results_counter).zfill(digits),self.result_len),end="\r")
        while True:
            if not self.response:
                return
            for card in self.response["data"]:
                results_counter += 1
                if card["name"] in self.collection:
                    #remove list from collection, add it to results cards
                    self.result_cards.extend(self.collection.pop(card["name"]))
            print("Filtering:{}/{}".format(str(results_counter).zfill(digits),self.result_len),end="\r")
            if not self.response["has_more"]:
                print()
                break
            else: 
                time.sleep(.2)
                self.response = requests.get(self.response["next_page"]).json()
