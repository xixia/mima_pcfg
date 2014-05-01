import sys

script, filename, outname, threshold = sys.argv

f = open(filename, 'r')
fo = open(outname + '.txt', 'w')

min_amt = int(threshold)
total = int(f.readline())

for l in f.readlines():
  sp = l.split()

  word_freq = int(sp[1])
  if (word_freq < min_amt):
    total -= word_freq
  else:
    fo.write('%s' % l)

fo.write('%d\n' % total)
