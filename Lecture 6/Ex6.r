# function to calculate stationary distribution of a transition matrix
library(matlib)

st_d_from_Q <- function(Q) {
    dim = sqrt(length(Q))
    b = matrix(c(1,rep(0,dim-1)),nrow=dim,byrow=T)
    Q[,1] <- rep(1,dim)
    print("The solution is the following:")
    return(matlib::Solve(t(Q), b))
}

st_d_from_pi_t_Q <- function(pi_t, Q) {
    q = -diag(Q)
    pi = (pi_t/q)/sum(pi_t/q)
    return(pi)
}

# ex 5
# 
rate = 50
Q = matrix(rep(0,31*31),nrow=31)
for (i in 2:31) {
    Q[i-1,i] = rate
    Q[i-1,i-1] = -50-(i-2)
    Q[i,i-1] = i-1
}
Q[31,31] = -30


# rates
rates1 = c(12,20,29,41)
rates2 = c(12,20,29)
rate1 = 1/sum(rates1)
rate2 = 1/sum(rates2)
p1 = dexp(90,rate1)
p2 = dexp(60,rate2)
Q = matrix(rep(0,4*4),nrow=4)
Q[]