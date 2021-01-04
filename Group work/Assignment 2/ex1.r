library(stringi)

freq <- read.table('./data/Englishcharacters.txt')
message <- paste(readLines("./data/messages.txt"))[1]

# decode function
decode <- function(message, freqs, iters) {
    # message separated by "" to iterate
    msg <- strsplit(message, "")[[1]]

    # identity function
    fvals <- 1:27
    letters <- c("a", "b", "c", "d",
                "e", "f", "g", "h", 
                "i", "j", "k", "l", 
                "m", "n", "o", "p", 
                "q", "r", "s", "t", 
                "u", "v", "w", "x", 
                "y", "z", " ")
    names(fvals) <- letters
    f <- function(c) return(fvals[c])

    # score function
    score <- function(fun) {
        p <- 1
        for (i in 2:length(msg)) {
            if (freq[fun(msg[i-1]),fun(msg[i])] != 0) {
                p <- p * freq[fun(msg[i-1]),fun(msg[i])]
            } 
        }
        return(p)
    }

    for (i in 1:iters) {
        # values for the function
        fvals_n <- 1:27

        # randomly choose 2 numbers and replace the 2 chosen vals in a copy of letters
        choice_1 <- as.integer(runif(1, min=1, max=27))
        choice_2 <- as.integer(runif(1, min=1, max=27))
        letters_n <- letters
        letters_n[choice_1] <- letters[choice_2]
        letters_n[choice_2] <- letters[choice_1]
        names(fvals_n) <- letters_n

        # f asterisk
        f_n <- function(c) return(fvals_n[c])
        scr <- score(f_n)/score(f)
        print(scr)
        cond <- runif(1) <= scr
        rnd <- runif(1)
        if (is.na(cond) == TRUE) {
            for (l in 1:length(msg)) {
                msg[l] <- names(f(msg[l]))
            }
        } else if (rnd <= scr){
            letters <- letters_n
            names(fvals) <- letters
            f <- function(c) return(fvals[c])
            for (l in 1:length(msg)) {
                msg[l] <- names(f(msg[l]))
            }
        } else if (rnd >= scr){
            for (l in 1:length(msg)) {
                msg[l] <- names(f(msg[l]))
            }
        }

    }
    return(stri_paste(msg,collapse=''))
}
decode(message,freq,100)