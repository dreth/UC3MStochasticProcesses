# exercise 3a
library(ggplot2)

ar_1 <- function(theta, sigma_sq, x_n_1, len) {
    sim_values <- rep(0,len+1)
    sim_values[1] <- x_n_1
    for (i in 1:len) {
        sim_values[i+1] <- theta*sim_values[i] + rnorm(1,0,sigma_sq)
    }
    return(sim_values)
}

runs <- 1000
theta <- seq(-1,1,(1-0)/runs)
results <- rep(0, length(theta))
for (i in 1:length(results)) {
    results[i] <- mean(ar_1(theta[i],1,100,10000))
}
results <- data.frame(results)
results$theta <- theta
png('./UC3MStochasticProcesses/Lecture 3/results.png',height=1000, width=1000)
ggplot(results, aes(x=theta, y=result))
dev.off()
