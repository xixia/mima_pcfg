f = open('pinyin_frequency.txt', 'r')
f_out = open('all_pinyin.txt', 'w')
fo_freq = open('freq_pinyin.txt', 'w')

pinyin = {}
total = 0

for l in f.readlines():
  # split into different columns. important one is the fifth column.
  sections = l.split(None, 5)

  if (len(sections) >= 5):
    poss = sections[4].split('/')
    num = int(sections[2])

    for p in poss:
      if (p[-1].isdigit()):
        p = p[:-1]

      pinyin.setdefault(p.lower(), 0)
      pinyin[p.lower()] += num

    total += num

for p in pinyin.keys():
  f_out.write('%s\n' % p)
  fo_freq.write('%s %s\n' % (p, pinyin[p]))

fo_freq.write('%d\n' % total)