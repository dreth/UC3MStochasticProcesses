# importing libraries
import numpy as np
from copy import deepcopy
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import words

# Importing the matrix with the frequencies
freq =  np.loadtxt('./data/Englishcharacters.txt', usecols=range(27))

# transformation function for table values
def transf_log(table):
    return np.log(table + 1)

# applying the transformation function
freq = transf_log(freq)

# importing the messages and only selecting the 
# message with index 0, as this is the one corresponding
# to group 1
with open('./data/messages.txt') as f:
    message = f.readlines()[0].replace('\n','')

# decode function
def decode(message, freqs, iters, check_words=True):
    """
    Function to decode a message enconded 
    using a substitution cipher utilizing the
    Metropolis-Hastings algorithm.

    Params:
    message = string to decode
    freqs = frequency table for transitions of letters
            to input
    iters = amount of iterations to perform
    """
    # dictionary to organize the iterations
    # the score and the result of the attempt
    # to decode the message corresponding to that
    # iteration
    msg_iters = {}

    # defining the identity function
    # all letters to be used excluding spaces
    letters = ["a", "b", "c", "d",
                "e", "f", "g", "h", 
                "i", "j", "k", "l", 
                "m", "n", "o", "p", 
                "q", "r", "s", "t", 
                "u", "v", "w", "x", 
                "y", "z"]
    # creating a copy of the original letters
    # to use as key for the dictionaries
    init_letters = deepcopy(letters)
    # creating a dictionary with init_letters as keys
    # and letters as values
    cd = {l:d for l,d in zip(init_letters,letters)}
    # every time we update with {' ':' '} we add the space
    # to the dictionary
    cd.update({' ':' '})
    # define a function that just uses the previous
    # dictionary to seek the letters
    def f(c):
        return cd[c]
    
    # this dictionary and subsequent function maps each letter
    # to a column/row in the freq matrix, ex: 'a':0, 'b':1 
    fvals = np.array([x for x in range(len(letters))])
    cd_map = {l:v for l,v in zip(letters,fvals)}
    cd_map.update({' ':26})
    def f_map(c):
        return cd_map[c]

    # score function uses sum of logs
    def score(fun):
        p = 0
        for i in range(1,len(msg)):
            p = p + freqs[f_map(fun(msg[i-1])),f_map(fun(msg[i]))]
        return p
    
    # converting the message to a list in order to
    # go through the letters in pairs
    msg = list(message)

    # letters list, this one shall be modified
    # every time the score passes the test
    letters_n = deepcopy(letters)

    # loop iters amount of times
    for i in range(iters):
        # randomly choose 2 numbers and replace the 2 chosen 
        # vals in a copy of letters
        ch1 = np.random.randint(0,len(letters))
        ch2 = np.random.randint(0,len(letters))
        plc1 = deepcopy(letters_n[ch1])
        plc2 = deepcopy(letters_n[ch2])
        letters_n[ch1] = plc2
        letters_n[ch2] = plc1

        # create the dictionary for the f* function
        cd_n = {l:v for l,v in zip(init_letters,letters_n)}
        # add the space to it after scramble
        cd_n.update({' ':' '})
        # f* definition
        def f_n(c):
            return cd_n[c]
    
        # calculating the score for each function and its ratio
        scr_f = score(f)
        scr_fn = score(f_n)
        a = np.exp(scr_fn - scr_f)
        # test if a random number is lower than min(a, 1)
        cond = np.random.rand() < min(a,1)
        # if condition is true
        if cond:
            # replacing the letters list with the one from f*
            letters = deepcopy(letters_n)
            # updating the dictionary with the new letters list after replacing
            cd = {l:v for l,v in zip(init_letters,letters)}
            cd.update({' ':' '})
            # f re-definition
            def f(c):
                return cd[c]
            # replacing the letters in the message using 
            # the new f replaced by f*
            for k in range(len(msg)):
                msg[k] = f(msg[k])
            # adding score and joining the message to the dictionary
            # to then transform into a dataframe
            msg_iters[i] = (a,''.join([x for x in msg]))

            # we separate the message by words
            msg_list = msg_iters[i][1].split(' ')
            # we test 5 random words to see if they are actually words 
            # present in the word corpus
            conds = [np.random.choice(msg_list) in words.words() for x in range(5)]
            # if check words == True
            if check_words == True:
                # we break the loop if the 5 true words are found
                if False not in conds:
                    print('Cipher used:\n')
                    print(f'{cd}')
                    print(f'\nfound at iteration: {i}\nMessage (may contain wrong letters):')
                    return msg_iters[i]
            # otherwise
            else:
                # we print the iteration number and message only 
                # when the cipher changes
                print(f'iteration #{i}:\n')
                print(f'{msg_iters[i][1]}\n')
        # if condition is false
        else:
            # resetting the letters after a failed score comparison
            letters_n = deepcopy(letters)
            # apply the f function to the message instead
            for k in range(len(msg)):
                msg[k] = f(msg[k])
        
        # reset the message
        msg = list(message)

    # put the information in a dataframe, iters, score and the messages
    df = {'iter':[it for it in msg_iters.keys()],
          'score':[msg[0] for msg in msg_iters.values()],
          'msg':[msg[1] for msg in msg_iters.values()]}
    # return the dataframe in case the loop was never broken
    return pd.DataFrame(df)

decode(message, freq, 100000, check_words=False)