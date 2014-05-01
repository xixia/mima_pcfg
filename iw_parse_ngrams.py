import sys
import re

script, filename, outname = sys.argv

f = open(filename, 'r')
fo = open(outname + '.txt', 'w')

_digits = re.compile('\d')
_under = re.compile('_')
prev = ['', '']
prev_outword = ''
valid = False
all_word = []

num_print = 1
total_words = 0

all_words = {}

for line in f.readlines():
  linesplit = line.split()

  if ((linesplit[0] == prev[0])):
    if (valid):
      all_word.append(linesplit)
    prev = linesplit
    continue
  else:
    # this is where stuff gets recorded.
    if (valid):
      sum_word = 0
      for i in range(1, num_print + 1):
        sum_word += int(all_word[-1 * i][2])
      # fo.write('%d\n' % sum_word)
      all_words[prev_outword] += sum_word
      total_words += sum_word
    all_word = []

  prev = linesplit

  # this will contain the correctly formatted word.
  outword = linesplit[0]

  # check if it contains numbers or an underscore.
  if (bool(_digits.search(linesplit[0])) or bool(_under.search(linesplit[0]))):
    valid = False
    continue
  if (not linesplit[0].isalpha()):
    num_apos = linesplit[0].count("'")
    if (num_apos != 1):
      valid = False
      continue
    else:
      outword = linesplit[0].replace("'", "")
  
  # passes tests as a word. print it out.
  valid = True
  all_word.append(linesplit)
  prev_outword = outword.lower()
  # fo.write('%s,' % outword.lower())
  all_words.setdefault(prev_outword, 0)

if (valid):
  sum_word = 0
  for i in range(1, num_print + 1):
    sum_word = int(all_word[-1 * i][2])
  # fo.write('%d\n' % sum_word)
  all_words[prev_outword] += sum_word
  total_words += sum_word

for key in all_words:
  fo.write('%s,%s\n' % (key, all_words[key]))

fo.write('%d\n' % total_words)