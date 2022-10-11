
def show(p):
  [print(l,*d) for l,d in zip(L,p)]
  # for i in (0,1,2):
  #   print(L[i], *p[i])

def H(n, src, tmp, dst):
  if n > 0:
    H(n-1, src, dst, tmp)
    print(f'move disk {n} from {L[src]} to {L[dst]}');
    d = p[src].pop()
    p[dst].append(d)
    show(p)
    H(n-1, tmp, src, dst)

def main():
  global L, p
  n = 3
  L = 'abc'
  p = [list(range(n,0,-1)), [], []]
  print(f'\nTowers of Hanoi for {n} disks:')
  show(p)
  H(n, 0, 1, 2)