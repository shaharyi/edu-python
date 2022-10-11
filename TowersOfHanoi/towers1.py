def H(n, src, tmp, dst):
  if n > 0:
    H(n-1, src, dst, tmp)
    print(f'move disk {n} from {src} to {dst}')
    H(n-1, tmp, src, dst)

def main():
  n=3
  print(f'Towers of Hanoi for {n} disks:')
  H(n, 'a', 'b', 'c')
