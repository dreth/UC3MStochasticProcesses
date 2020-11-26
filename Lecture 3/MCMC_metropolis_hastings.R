x_0 <- 0 # initial value
x <- c(x_0) # vector x
a <- 1 # limit of a for uniform dist
mean_x <- c() # mean of x to plot convergence
sd_x <- c() # sd of x to plot convergence

# f(y)q(x|y) / f(x)q(y|x)
f_q <- function(y,x,a) {
    return(exp((x^2 - y^2)/2))
}

for (i in 1:1e4) {
    prev_x <- x[i] # previous value
    yn <- runif(1, min=prev_x - a, max=prev_x + a) # yn
    rho <- min(f_q(yn,prev_x, a),1) # rho function
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
