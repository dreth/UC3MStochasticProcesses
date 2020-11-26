matrixpower <- function(M,k) {
  # ARGUMENTS:
  # M: square matrix 
  # k: exponent
  if(dim(M)[1]!=dim(M)[2]) return(print("Error: matrix M is not square"))
  if (k == 0) return(diag(dim(M)[1]))  # if k=0 returns the identity matrix
  if (k == 1) return(M)
  if (k > 1)  return(M %*% matrixpower(M, k-1)) # if k>1 recursively apply the function
}

