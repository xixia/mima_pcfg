# the inputs must be of only the passwords in a randomized order.

files = ['70yx.txt', 'uuu9.txt', 'csdn.sql']
counts = [9072966, 9458105, 6428630]

file_test = ['70yx_cor.txt']
file_count = [9072966]

for i, filename in enumerate(file_test):
  f = open(filename, 'r')
  f_prefix = filename.split('.')
  f_train = open(f_prefix[0] + '_train.txt', 'w')
  f_test = open(f_prefix[0] + '_test.txt', 'w')

  all_lines = f.readlines()
  num_lines = len(all_lines)
  maxnum_test = int(num_lines * .2)
  maxnum_train = int(num_lines * .8)

  all_lines_under = []
  for w in all_lines:
    all_lines_under.append(w.lower())

  training = set(all_lines_under[0:maxnum_train])
  testing = set(all_lines_under[maxnum_train:])

  list_train = list(training)
  list_test = list(testing)

  for p in list_train:
    f_train.write(p)
  for p in list_test:
    f_test.write(p)
