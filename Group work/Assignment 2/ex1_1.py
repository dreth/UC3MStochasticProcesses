from random import choice
import numpy as np
from copy import deepcopy
import pandas as pd

freq =  np.loadtxt('./data/Englishcharacters.txt', usecols=range(27))

def transf_minmax(table,a,b):
    return (b-a)*((table - np.min(table))/(np.max(table) - np.min(table))) + a 

def transf_log(table):
    return np.log(table + 1)

freq = transf_log(freq)
 
with open('./data/messages.txt') as f:
    message = f.readlines()[0].replace('\n','')

def decode(message, freqs, iters):
    # messages per iteration
    msg_iters = {}
    # identity function
    fvals = np.array([x for x in range(27)])
    letters = ["a", "b", "c", "d",
                "e", "f", "g", "h", 
                "i", "j", "k", "l", 
                "m", "n", "o", "p", 
                "q", "r", "s", "t", 
                "u", "v", "w", "x", 
                "y", "z", " "]
    init_letters = deepcopy(letters)
    cd = {l:v for l,v in zip(letters,fvals)}
    init_cd = deepcopy(cd)
    def f(c):
        return cd[c]
    
    # score function
    def score(fun):
        p = 0
        for i in range(1,len(msg)):
            p = p + freq[fun(msg[i-1]),fun(msg[i])]
        return p
    
    # msg to list
    msg = list(message)
    
    for i in range(iters):

        # randomly choose 2 numbers and replace the 2 chosen vals in a copy of letters
        ch1 = np.random.randint(1,27)
        ch2 = np.random.randint(1,27)
        letters_n = deepcopy(letters)
        letters_n[ch1] = letters[ch2]
        letters_n[ch2] = letters[ch1]
        cd_n = {l:v for l,v in zip(letters_n,fvals)}
        
        # f asterisk
        def f_n(c):
            return cd_n[c]

        #loop with scores
        scr = score(f_n)/score(f)
        cond = np.random.rand() <= scr
        if cond:
            letters = deepcopy(letters_n)
            cd = {l:v for l,v in zip(letters,fvals)}
            for k in range(len(msg)):
                msg[k] = letters[init_cd[msg[k]]]
            msg_iters[i] = ''.join([x for x in msg])
        else:
            pass
        
    
    # put in a dataframe
    df = {'iter':[it for it in msg_iters.keys()], 
          'msg':[msg for msg in msg_iters.values()]}
    return pd.DataFrame(df)


result = decode(message,freq, 10000)
result.to_csv('result.csv')
