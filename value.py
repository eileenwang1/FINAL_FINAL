import random

numbers=[]

class Card():
    def __init__(self, suit, rank):
        self.suit = suit # takes value in 1,2,3,4
        self.suit_printed = [u'\u2660', u'\u2661', u'\u2662', u'\u2663'][self.suit - 1]
        self.rank = rank
        self.rank_printed = ['2','3','4','5','6','7','8','9','10','J','Q','K','A'][self.rank - 2]

    def __repr__(self):
        return self.suit_printed + self.rank_printed
    
    def __eq__(self, other):
        if type(other) == int:
            return  self.rank == other
        return self.rank == other.rank
    
    def __gt__(self, other):
        if type(other) == int:
            return  self.rank == other
        return self.rank > other.rank
    
    def __lt__(self, other):
        if type(other) == int:
            return  self.rank == other
        return self.rank < other.rank

def shuffle():
    deck=[]
    for suit in range(1, 5):
        for rank in range(2, 15):
            deck.append(Card(suit, rank))
    
    return deck

def value_seven(cards):
    flush, straight = False, False
    vlist = []
    value = 0
    string = ""
    suits,numbers,flush_nums = [],[],[]
    for i in cards:
        numbers.append(i.rank)
        suits.append(i.suit)
    if 14 in numbers:
        numbers.append(1)
    
    for i in suits:
        if suits.count(i) >= 5:
            flush=True
            for j in cards:
                if j.suit == i:
                    flush_nums.append(j.rank)
                    flush_suit = i
            if 14 in flush_nums:
                flush_nums.append(1)
    
    appear_dic = {1:[],2:[],3:[],4:[]}
    
    for card in cards:
        appear_times = numbers.count(card.rank)
        appear_dic[appear_times].append(card)

    singles,pairs,trips,quads = appear_dic[1],appear_dic[2],appear_dic[3],appear_dic[4]
    singles.sort(reverse = True)
    pairs.sort(reverse = True)
    trips.sort(reverse = True)
    quads.sort(reverse = True)
    pairs = [pairs[i] for i in range(0,len(pairs),2)]
    trips = [trips[i] for i in range(0,len(trips),3)]
    quads = [quads[i] for i in range(0,len(quads),4)]
    len_pairs, len_trips = len(pairs), len(trips)

    if trips == [] and quads == []: #no trips and no quads
        if len_pairs == 1:
            vlist.append(pairs[0])
            vlist.append(singles[:3])
            value = 2
            string = "a pair of {0}s with {1}".format(vlist[0].rank_printed,vlist[1][0].rank_printed)
        elif len_pairs >= 1:
            vlist.append(pairs[:2])
            if len_pairs == 3:
                singles.append(pairs[2])
            singles = sorted(singles, reverse=True)
            vlist.append(singles[0])
            value=3
            string="{0}s and {1}s".format(vlist[0][0].rank_printed,vlist[0][1].rank_printed,vlist[1].rank_printed)
        elif pairs == []:
            vlist.append(singles)
            value = 1
            string = "{} high".format(vlist[0][0].rank_printed)
            
    elif quads == [] : #have at least a trip
        if len_trips == 1 and len_pairs == 0:
            vlist.append(trips[0])
            vlist.append(singles[:3])
            value = 4
            string = "three {0}s with {1}".format(vlist[0].rank_printed,vlist[1][0].rank_printed)
        elif len_trips == 1 and len_pairs >= 1:
            vlist.append(trips[0])
            vlist.append(pairs[0])
            value = 7
            string="{0}s full of {1}s".format(vlist[0].rank_printed,vlist[1].rank_printed)
        elif len_trips == 2:
            vlist.append(trips[0])
            vlist.append(trips[1])
            value = 7
            string = "{0}s full of {1}s".format(vlist[0].rank_printed,vlist[1].rank_printed)
            
    else: #have a quads
        vlist.append(quads[0])
        singles = singles + pairs + trips
        singles = sorted(singles,reverse=True)
        vlist.append(singles[0])
        value = 8
        string = "four {0}s with {1}".format(vlist[0].rank_printed,vlist[1].rank_printed)
    
    if flush:
        vlist=[]
        straightFlush = False
        for i in range (10,0,-1):
            if i in flush_nums and (i+1) in flush_nums and (i+2) in flush_nums\
               and (i+3) in flush_nums and (i+4) in flush_nums:
                straightFlush=True
                for card in cards:
                    if card.rank == i + 4 and card.suit == flush_suit:
                        vlist.append(card)
                        break
                break
        if straightFlush:
            value = 9
            string = "{} high straight flush".format(vlist[-1].rank_printed)
            if vlist[0] == 14:
                value = 10
                vlist = []
                string = "Royal Flush"
        elif value < 6:
            for card in cards:
                if card.suit == flush_suit:
                    vlist.append(card)
            vlist.sort(reverse = True)
            value = 6
            string = "{} high flush".format(vlist[0].rank_printed)
             
    elif value < 5:
        straight = False
        for i in range (10,0,-1):
            if i in numbers and (i+1) in numbers and (i+2) in numbers\
               and (i+3) in numbers and (i+4) in numbers:
                vlist = []
                straight = True
                for card in cards:
                    if card.rank == i + 4:
                        vlist.append(card)
                        break
                break

        if straight:
            value = 5
            string = "{} high straight".format(vlist[0].rank_printed)
    
    return value,vlist,string

if __name__=='__main__':
    deck = shuffle()
    for i in range(20):
        random.shuffle(deck)
        a = deck[:7]
        print(i,a)
        print(valueSeven(a))
        
