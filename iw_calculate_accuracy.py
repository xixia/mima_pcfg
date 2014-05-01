# ----------------------------------------------------------------------- #
# to execute:
# python iw_calculate_accuracy.py [text file of generated passwords] [text file of known test passwords] [file name to print information to]



import sys

script, generated, test, outname = sys.argv

ftest = open(test, 'r')
fgen = open(generated, 'r')
fo = open(outname + '.txt', 'w')

pw = []
total_pw = 0

for line in ftest.readlines():
  pw.append(line.rstrip().lower())
  total_pw += 1

pw = set(pw)
print 'completed loading test passwords'
found_pw = []

total_correct = 0
total_gen = 0
for line in fgen.readlines():
  word = line.rstrip().lower()
  if (word in pw):
    total_correct += 1
    found_pw.append(word)
    print word
  total_gen += 1

found_pw = set(found_pw)

# going to print to an output file all of the passwords in the test file, in sorted order. passwords with asterisk by them means they were found by algorithm.
sorted_pw = sorted(list(pw))
for w in sorted_pw:
  if w in found_pw:
    fo.write('%s *\n' % w)
  else:
    fo.write('%s\n' % w)


print 'total words generated', total_gen
print 'total correct', total_correct
print 'total words in test file', total_pw