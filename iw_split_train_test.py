# the inputs must be of only the passwords in a randomized order.
# usage: python iw_split_train_test.py [password file to split]

import sys

# files = ['70yx.txt', 'uuu9.txt', 'csdn.sql']
# counts = [9072966, 9458105, 6428630]

# file_test = ['70yx_cor.txt']
# file_count = [9072966]

# for i, filename in enumerate(file_test):

script, filename = sys.argv

# setup.
f = open(filename, 'r')
f_prefix = filename.split('.')
f_train = open(f_prefix[0] + '_train.txt', 'w')
f_pure = open(f_prefix[0] + '_train_pure.txt', 'w')
f_test = open(f_prefix[0] + '_test.txt', 'w')

# read in all of the lines of the file. calculate the 80-20 ratio.
all_lines = f.readlines()
num_lines = len(all_lines)
maxnum_train = int(num_lines * .8)
maxnum_test = num_lines - maxnum_train

testset = {}
trainset = {}

# lowercase all of the passwords. DO NOT NEED TO DO THIS ELSEWHERE.
# when going through and lowercasing, put them into dictionary to keep track of frequency.
all_lines_under = []
for idx, word in enumerate(all_lines):
  w = word.rstrip().lower()
  if (idx < maxnum_train):
    trainset.setdefault(w, 0)
    trainset[w] += 1
  else:
    testset.setdefault(w, 0)
    testset[w] += 1

# sort by values for both lists.
trainsort = sorted(trainset, key=trainset.get, reverse = True)
testsort = sorted(testset, key=testset.get, reverse = True)

# print out the words and their frequency.
for p in trainsort:
  f_train.write('%s %d\n' % (p, trainset[p]))
  f_pure.write('%s\n' % p)
  
for p in testsort:
  f_test.write('%s %d\n' % (p, testset[p]))