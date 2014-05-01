f_words = open('words', 'r')
f_en = open('en.txt', 'r')
fo = open('freq_eng.txt', 'w')

accept = []
for word in f_words.readlines():
  accept.append(word.rstrip().lower())

accept = set(accept)

total = 0

for line in f_en.readlines():
  split = line.split()

  if split[0].lower() in accept:
    fo.write('%s %s\n' % (split[0].lower(), split[1]))
    total += int(split[1])

fo.write('%d\n' % total)

7,258,372