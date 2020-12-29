matrixpower <- function(M,k) {
  # ARGUMENTS:
  # M: square matrix 
  # k: exponent
  if(dim(M)[1]!=dim(M)[2]) return(print("Error: matrix M is not square"))
  if (k == 0) return(diag(dim(M)[1]))  # if k=0 returns the identity matrix
  if (k == 1) return(M)
  if (k > 1)  return(M %*% matrixpower(M, k-1)) # if k>1 recursively apply the function
}

P <- c(0.05, 0.25, 0.25, 0.3, 0.15,
        0.4, 0.05, 0.05, 0.2,  0.3,
        0.2,  0.2,    0, 0.3,  0.3,
        0.3,  0.2,  0.2, 0.1,  0.2,
        0.2, 0.25,  0.3, 0.1, 0.15)
P <- matrix(P,nrow=5,byrow=T)

dist <- matrixpower(P, 200)

result <- mean(matrix(c(5,6,6,4,4), nrow=1, byrow=T)%*%dist)
result

