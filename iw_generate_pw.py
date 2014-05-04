# usage: python iw_generate_pw.py [prefix of all the info files] [minimum amount to generate] [training file] [output file]

import sys
import Queue

num_tab = {}
rand_tab = {}
pinyin_tab = {}
eng_tab = {}

trained_pw = ()

def load_prob(filename):
  f = open(filename, 'r')
  tab = {}

  for line in f.readlines():
    spl = line.rstrip().split()
    length = int(spl[0])
    prob = float(spl[2])

    tab.setdefault(length, {})
    tab[length].setdefault(prob, [])
    tab[length][prob].append(spl[1])

  return tab

def recurse_find(comp, ind, curr, poss):
  global trained_pw
  comp_len = len(comp)

  # base case...
  if (ind == comp_len):
    if (curr not in trained_pw):
      poss.append(curr)
    return poss

  # have group, ind, sorted_prob
  prob = comp[ind]['sorted_prob'][comp[ind]['ind']]

  # CONSIDER THE CASE WHERE IT DOESN'T EXIST...
  for item in comp[ind]['group'][prob]:
    poss = recurse_find(comp, ind + 1, curr + item, poss)

  return poss

# ----------------------------------------------------------------------- #
# start of the main script.
# ----------------------------------------------------------------------- #

script, prefix, min_generate, training, outname = sys.argv

# load in probability tables
num_tab = load_prob(prefix + '_num.txt')
eng_tab = load_prob(prefix + '_eng.txt')
pinyin_tab = load_prob(prefix + '_pinyin.txt')
rand_tab = load_prob(prefix + '_rand.txt')
spec_tab = load_prob(prefix + '_spec.txt')

fstruct = open(prefix + '_structs.txt', 'r')

fo = open(outname + '.txt', 'w')

recycle = []
poss = []

pq = Queue.PriorityQueue(0)

# should construct the priority queue of the structures
for line in fstruct.readlines():
  comp = []

  s_present = line.find('s');
  if (s_present != -1):
    continue

  split = line.split()
  struct_len = len(split[0])

  struct_prob = float(split[1])
  p_prob = struct_prob

  i = 0
  max_comp_prob = 1
  while (i < struct_len):
    str_type = split[0][i]
    i += 1
    length = int(split[0][i])
    i += 1

    while ((i < struct_len) and split[0][i].isdigit()):
      length *= 10
      length += int(split[0][i])
      i += 1

    # have the correct type and length.
    corr_tab = []
    if (str_type == 'n'):
      # for numbers
      corr_tab = num_tab
    elif (str_type == 'r'):
      # for randoms
      corr_tab = rand_tab
    elif (str_type == 's'):
      # for special characters
      corr_tab = spec_tab
    elif (str_type == 'p'):
      # for pinyin
      corr_tab = pinyin_tab
    elif (str_type == 'e'):
      # for english
      corr_tab = eng_tab

    sorted_prob = sorted(corr_tab[length], reverse=True)
    comp.append({'group': corr_tab[length], 'ind': 0, 'sorted_prob': sorted_prob})
    max_comp_prob *= sorted_prob[0]
    ratio = 1

  pq.put((-(struct_prob * ratio), {'comp': comp, 'struct_prob': struct_prob, 'struct': split[0], 'max_comp_prob': max_comp_prob}))

# priority queue constructed. now onto generation.
# algorithm for generation: get the first item from the priority queue. generate the passwords according to the indices given.
# after generation, look at each component's index. increment one at each stage.
# put it into a list. sort the list. grab the one with the highest probability. put that respective index back on the pq.

# guess the passwords from training first.
ftrain = open(training, 'r')

num_generated = 0
min_gen = int(min_generate)
trained_pw = []
for line in ftrain.readlines():
  if (num_generated >= min_gen):
    break

  line = line.split()
  if (len(line) == 1):
    break

  fo.write('%s\n' % line[0])
  trained_pw.append(line[0])
  num_generated += 1

trained_pw = set(trained_pw)

# now go onto other generation. but do not repeat guesses...!!
while ((num_generated < min_gen) or (not pq.empty())):
  g = pq.get()

  prob = g[0]
  data = g[1]

  poss = recurse_find(data['comp'], 0, '', [])
  num_generated += len(poss)

  if (len(poss) != 0):
    for po in poss:
      fo.write('%s\n' % po)

  if (num_generated > min_gen):
    break

  new_prob = {}
  num_comp = len(data['comp'])
  for i in range(0, num_comp):
    ind = data['comp'][i]['ind'] + 1
    if (ind < len(data['comp'][i]['sorted_prob'])):
      curr_prob = data['comp'][i]['sorted_prob'][ind]
      for j in range(0, num_comp):
        if (j == i):
          continue
        other_ind = data['comp'][j]['ind']
        curr_prob *= data['comp'][j]['sorted_prob'][other_ind]
      new_prob.setdefault(curr_prob, [])
      new_prob[curr_prob].append(i)

  # if there is something in new_prob
  if (len(new_prob) > 0):
    sorted_prob = sorted(new_prob)
    change_ind = new_prob[sorted_prob[0]][0]
    data['comp'][change_ind]['ind'] += 1
    mod_prob = 1
    for c in data['comp']:
      mod_prob *= c['sorted_prob'][c['ind']]

    ratio = mod_prob / data['max_comp_prob']
    prob = -(ratio * data['struct_prob'])
    pq.put((prob, data))

# should do the grammar analysis recursively.
# for line in fstruct.readlines():
#   split = line.split()

#   struct_len = len(split[0])
#   poss = recurse_find(split[0], 0, '', poss)

# each of the grammatical structures have a probability.
# each of the components have probabilities associated with them.
# what to do: maintain a priority queue.
# initially, put all of the structures onto the queue -> should have probability
# equal to the probability of the structure multiplied by the probability of the first choice for each.

# what needs to be done:
# load in the probability tables for random, pinyin, english, and numbers (SOMETHING TO CONSIDER: when creating the probability tables, also fill in for the values that didn't occur)
# load in structures.
# iterate through structures in order, grabbing from the correct tables.