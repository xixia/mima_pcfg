# ----------------------------------------------------------------------- #
# to execute:
# python iw_calculate_accuracy.py [text file of generated passwords] [text file of known test passwords] [file name to print information to]


import sys

script, generated, test, dataname = sys.argv

ftest = open(test, 'r')
fgen = open(generated, 'r')
fo = open(dataname + '.txt', 'w')

pw = {}
total_pw = 0

# test file is in the format of pw freq per line.
for line in ftest.readlines():
  line = line.rsplit(' ', 1)
  w = line[0]
  freq = int(line[1])

  pw[w] = freq
  total_pw += freq

print 'completed loading test passwords'
found_pw = {}

total_correct = 0
total_gen = 0
for line in fgen.readlines():
  word = line.rstrip().lower()      # should lower, esp for jtr stuff.

  if (word in pw) and (word not in found_pw):
    total_correct += pw[word]
    found_pw[word] = 1
  
  # not listing each password.
  fo.write('%d %f\n' % (total_correct, float(total_correct) / total_pw))

  # listing each password.
  # fo.write('%s %d %f\n' % (word, total_correct, float(total_correct)/total_pw))
  total_gen += 1

# found_pw = set(found_pw)

# # going to print to an output file all of the passwords in the test file, in sorted order. passwords with asterisk by them means they were found by algorithm.
# sorted_pw = sorted(list(pw))
# for w in sorted_pw:
#   if w in found_pw:
#     fo.write('%s *\n' % w)
#   else:
#     fo.write('%s\n' % w)


print 'total words generated', total_gen
print 'total correct', total_correct
print 'total words in test file', total_pw