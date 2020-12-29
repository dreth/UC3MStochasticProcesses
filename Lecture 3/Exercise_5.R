x_0 <- 0 # initial value
x <- c(x_0) # vector x
a <- 0.02 # limit of a for uniform dist
mean_x <- c() # mean of x to plot convergence
sd_x <- c() # sd of x to plot convergence

# f(y)q(x|y) / f(x)q(y|x)
f_q <- function(y,x) {
    top <- exp(((-(y-1))^2)/2) + exp(((-(y-4))^2)/2)
    bottom <- exp(((-(x-1))^2)/2) + exp(((-(x-4))^2)/2)
    return(top/bottom)
}

for (i in 1:1e4) {
    prev_x <- x[i] # previous value
    yn <- runif(1, min=0, max=5) # yn
    rho <- min(f_q(yn,prev_x),1) # rho function
    u <- runif(1) # random number between 0 and 1

    # return x_n, next value
    if (u < rho) {
        x[i+1] <- yn
    } else {
        x[i+1] <- prev_x
    }
    
    # adding elements to plot convergence
    mean_x[i] <- mean(x)
    sd_x[i] <- sd(x)
}

hist(x)
plot(mean_x)
plot(sd_x)

