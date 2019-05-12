# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
"""
import pickle

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = []
        """
        ["1st_line", "2nd_line", "3rd_line", ...]
        Example:
        "How are you?\nI am fine.\n" will be stored as
        ["How are you?", "I am fine." ]
        """
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0

        """ self.index is a dictionary with word as key and
        list of tuples (line#, msg_line) as value
        {word1: [(line_number_of_1st_occurrence, 'msg1'),
                 (line_number_of_2nd_occurrence, 'msg2'),
                 ...]
         word2: [(line_number_of_1st_occurrence, 'msg1'),
                 (line_number_of_2nd_occurrence, 'msg2'),
                  ...]
         ...
        }
        """

    def get_total_words(self):
        return self.total_words

    def get_msg_size(self):
        return self.total_msgs

    def get_msg(self, n):
        return self.msgs[n]

    # implement
    def add_msg(self, m):
        """
        m: the message to add

        updates self.msgs and self.total_msgs
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        self.msgs.append(m)
        self.total_msgs += 1

        # ---- end of your code --- #
        return

    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    # implement
    def indexing(self, m, l):
        """
        updates self.total_words and self.index
        m: message, l: current line number
        """

        # IMPLEMENTATION
        # ---- start your code ---- #
        #split m into list of words

        if len(m) > 2:
            #remove all the punctuations:
            #split into all list, remove all the punctuations
            all_list = []
            for i in m:
                if i in ",.?'!;:":
                    continue
                else:
                    all_list.append(i)

            #join the list again (base on "")
            new_str = "".join(all_list)
            #split the string again (base on " ")
            words_in_m = new_str.split(" ")

            #fit into the dict.
            for i in words_in_m:
                #pay attention to where there is not a return value
                check_value = self.index.get(i,[])
                check_value.append((l,m))
                self.index[i] = check_value

        #i see no point of putting " " or "I." into self.index
        #in order to save memory...

        # ---- end of your code --- #
        return

    # implement: query interface

    def search(self, term):
        """
        return a list of tuple.
        Example:
        if index the first sonnet (p1.txt),
        then search('thy') will return the following:
        [(7, " Feed'st thy light's flame with self-substantial fuel,"),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (12, ' Within thine own bud buriest thy content,')]
        """
        msgs = []
        # IMPLEMENTATION
        # ---- start your code ----
        #determine whether the term is a phrase
        set_to_return = set()
        term = term.strip()
        if " " in term:
            #the term is a phrase
            term_list = term.split(" ")
            for i in term_list:
                temp = self.index.get(i, -1)  # -1 means "search not found"
                if temp == -1:
                    return "search not found"
                else:
                    if len(set_to_return) != 0:
                        set_to_return = set_to_return & set(temp)
                    else:
                        set_to_return = set(temp)
                    if len(set_to_return) == 0:
                        return "search not found"
            msgs = list(set_to_return)

        else:
            msgs = self.index.get(term, -1) #-1 means "search not found"
            if msgs is [-1]:
                return "search not found"
            else:
                #to remove duplicate items:
                myset = set(msgs)
                msgs = list(myset)

        # ---- end of your code --- #
        return msgs



class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()

        # implement: 1) open the file for read, then call
        # the base class's add_msg_and_index
    def load_poems(self):
        """
        open the file for read, then call
        the base class's add_msg_and_index()
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        poems = open("AllSonnets.txt","r")
        while True:
            m = poems.readline()
            if len(m) == 0:
                break
            else:
                m = m.rstrip("\n")
                self.add_msg_and_index(m)
        poems.close()
        # ---- end of your code --- #
        return

    def get_poem(self, p):
        """
        p is an integer, get_poem(1) returns a list,
        each item is one line of the 1st sonnet

        Example:
        get_poem(1) should return:
        ['I.', '', 'From fairest creatures we desire increase,',
         " That thereby beauty's rose might never die,",
         ' But as the riper should by time decease,',
         ' His tender heir might bear his memory:',
         ' But thou contracted to thine own bright eyes,',
         " Feed'st thy light's flame with self-substantial fuel,",
         ' Making a famine where abundance lies,',
         ' Thy self thy foe, to thy sweet self too cruel:',
         " Thou that art now the world's fresh ornament,",
         ' And only herald to the gaudy spring,',
         ' Within thine own bud buriest thy content,',
         " And, tender churl, mak'st waste in niggarding:",
         ' Pity the world, or else this glutton be,',
         " To eat the world's due, by the grave and thee.",
         '', '', '']
        """
        poem = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        roman_p = self.int2roman[p] + "."
        roman_p_next = self.int2roman[p+1] + "."
        #access self.msgs
        start = self.msgs.index(roman_p)
        if roman_p_next in self.msgs:
            end = self.msgs.index(roman_p_next)
        else:
            end = len(self.msgs)

        poem = self.msgs[start:end]


        # ---- end of your code --- #
        return poem

    def get_poem_r(self, r):
        #parameter is a roman letter
        poem = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        roman_p = self.int2roman[p] + "."
        roman_p_next = self.int2roman[p+1] + "."
        #access self.msgs
        start = self.msgs.index(roman_p)
        if roman_p_next in self.msgs:
            end = self.msgs.index(roman_p_next)
        else:
            end = len(self.msgs)

        poem = self.msgs[start:end]


        # ---- end of your code --- #
        return poem

if __name__ == "__main__":
    '''
    sonnets = PIndex("AllSonnets.txt")
    # the next two lines are just for testing
    p3 = sonnets.get_poem(5)
    print(p3)
    s_love = sonnets.search("five wits")
    print(s_love)
    '''
    a = Index("name")
    print(a.name)

