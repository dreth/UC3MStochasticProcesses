import numpy as np
from copy import deepcopy
import pandas as pd
from nltk.corpus import words

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
    letters = ["a", "b", "c", "d",
                "e", "f", "g", "h", 
                "i", "j", "k", "l", 
                "m", "n", "o", "p", 
                "q", "r", "s", "t", 
                "u", "v", "w", "x", 
                "y", "z", " "]
    init_letters = deepcopy(letters)
    cd = {l:l for l,l in zip(init_letters,letters)}
    def f(c):
        return cd[c]
    
    # mapping letters to cols
    fvals = np.array([x for x in range(27)])
    cd_map = {l:v for l,v in zip(letters,fvals)}
    def f_map(c):
        return cd_map[c]

    # score function
    def score(fun):
        p = 0
        for i in range(1,len(msg)):
            p = p + freq[f_map(fun(msg[i-1])),f_map(fun(msg[i]))]
        return p
    
    # msg to list
    msg = list(message)

    # letters to modify the cipher
    letters_n = deepcopy(letters)

    for i in range(iters):

        # randomly choose 2 numbers and replace the 2 chosen vals in a copy of letters
        ch1 = np.random.randint(1,27)
        ch2 = np.random.randint(1,27)
        plc1 = deepcopy(letters_n[ch1])
        plc2 = deepcopy(letters_n[ch2])
        letters_n[ch1] = plc2
        letters_n[ch2] = plc1

        cd_n = {l:v for l,v in zip(init_letters,letters_n)}
        # f asterisk
        def f_n(c):
            return cd_n[c]

        #loop with scores
        scr = score(f_n)/score(f)
        cond = np.random.rand() <= scr
        if cond:
            letters = deepcopy(letters_n)
            cd = {l:v for l,v in zip(init_letters,letters)}
            for k in range(len(msg)):
                msg[k] = f(msg[k])
            msg_iters[i] = ''.join([x for x in msg])
        else:
            for k in range(len(msg)):
                msg[k] = f(msg[k])
            msg_iters[i] = ''.join([x for x in msg])
        
        try:
            msg_list = msg_iters[i].split(' ')
            fw = {'w1':np.random.choice(msg_list),
                  'w2':np.random.choice(msg_list),
                  'w3':np.random.choice(msg_list)}
            conds = {w_n:(w in words.words()) for w_n,w in fw.items()}
            if (len(fw) > 3) and (False not in conds.values()):
                print(f'found at iteration: {i}')
                print(msg_iters[i])
                print(f'words found: {[x for x in conds.values()]}')
                break
        except:
            continue
    
    # put in a dataframe
    df = {'iter':[it for it in msg_iters.keys()], 
          'msg':[msg for msg in msg_iters.values()]}
    return pd.DataFrame(df)

result = decode(message,freq, 20000)
result.to_csv('result.csv')
