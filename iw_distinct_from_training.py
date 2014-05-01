import sys

script, training, testing, output = sys.argv

ftrain = open(training, 'r')
ftest = open(testing, 'r')
fo = open(output + '.txt', 'w')

train_set = []

for line in ftrain.readlines():
  word = line.rstrip()
  train_set.append(word)

train_set = set(train_set)

for line in ftest.readlines():
  word = line.rstrip()

  if (word not in train_set):
    fo.write(word)
