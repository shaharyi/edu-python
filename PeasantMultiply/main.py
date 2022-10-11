# log2(n) = O(logn) for n the number
# log2(10^n) = nlog2(10) = O(n) for n digit number
def mult(m, n, a = 0):
    print(n)
    if n == 0:
      return a
    m *= 2
    n = n // 2
    if n % 2 != 0:
      a = a + m
    return mult(m, n, a)

r = mult(141, 35)
print(r)
