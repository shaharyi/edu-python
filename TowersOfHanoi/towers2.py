def H(n, src, tmp, dst):
  global L,p
  if n > 0:
    moves1 = H(n-1, src, dst, tmp)
    print(f'move disk {n} from {L[src]} to {L[dst]}')
    p[src] -= 1
    p[dst] += 1    
    print(p)
    moves2 = H(n-1, tmp, src, dst)
    return 1 + moves1 + moves2
  return 0

L = 'abc'
n=3
p = [n,0,0]
def main():
  print(p)
  moves = H(n, 0, 1, 2)
  print(f'It took {moves} moves')
