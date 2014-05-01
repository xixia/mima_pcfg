from operator import itemgetter
import string
import sys
import math

# ----------------------------------------------------------------------- #
# the main program at this point.
# ----------------------------------------------------------------------- #

root_pinyin = {}
root_eng = {}
shannon_pinyin = 0.0
shannon_eng = 0.0

# ----------------------------------------------------------------------- #
# sets all letters at a specific level to false.
# ----------------------------------------------------------------------- #

def set_level_false(root, lev):
  set_level_false_recurse(root, lev, 0)

# ----------------------------------------------------------------------- #
# performs recursion for finding all of the letters at the right level.
# ----------------------------------------------------------------------- #

def set_level_false_recurse(node, lev, curr):
  if (curr == lev):
    return
  poss = node['letters']
  for n in node['letters']:
    poss[n]['is_word'] = False
    set_level_false_recurse(poss[n], lev, curr + 1)

# ----------------------------------------------------------------------- #
# helper function. sets a specific word to being 'true'.
# ----------------------------------------------------------------------- #

def set_word_true(root, word):
  curr = root
  ind = 0
  for c in word:
    if c in curr['letters']:
      curr = curr['letters'][c]
      ind += 1

  if (ind == len(word)):
    curr['is_word'] = True

# ----------------------------------------------------------------------- #
# load in chinese dictionary.
# ----------------------------------------------------------------------- #

def load_pinyin_dict():
  global root_pinyin
  global shannon_pinyin

  all_pinyin = [line.rstrip() for line in open('freq_pinyin.txt', 'r')]
  total = int(all_pinyin[0])
  all_pinyin = all_pinyin[1:]
  trie_pinyin = {}
  trie_pinyin['is_word'] = False
  trie_pinyin['letters'] = {}
  trie_pinyin['prob'] = 0
  root_pinyin = trie_pinyin

  for info in all_pinyin:
    split = info.split()
    py = split[0]
    num = float(split[1])

    current_dict = root_pinyin
    for c in py:
      trie_pinyin = {}
      trie_pinyin['is_word'] = False
      trie_pinyin['letters'] = {}
      trie_pinyin['prob'] = 0

      current_dict['letters'].setdefault(c, trie_pinyin)
      current_dict = current_dict['letters'][c]
    current_dict['is_word'] = True
    prob = float(num) / total
    current_dict['prob'] = prob
    shannon_pinyin += prob * math.log(prob, 2)

  shannon_pinyin *= -1

# ----------------------------------------------------------------------- #
# load in english dictionary.
# ----------------------------------------------------------------------- #

def load_eng_dict():
  global root_eng
  global shannon_eng

  total_prob = 0

  all_eng = [line.rstrip() for line in open('freq_eng.txt', 'r')]
  total = int(all_eng[0])
  all_eng = all_eng[1:]
  trie_eng = {}
  trie_eng['is_word'] = False
  trie_eng['letters'] = {}
  trie_eng['prob'] = 0
  root_eng = trie_eng

  for info in all_eng:
    split = info.split()
    d = split[0]
    num = float(split[1])

    current_dict = root_eng
    for c in d:
      trie_eng = {}
      trie_eng['is_word'] = False
      trie_eng['letters'] = {}
      trie_eng['prob'] = 0

      current_dict['letters'].setdefault(c, trie_eng)
      current_dict = current_dict['letters'][c]
    current_dict['is_word'] = True
    prob = float(num) / total
    current_dict['prob'] = prob
    shannon_eng += prob * math.log(prob, 2)
    total_prob += prob

  shannon_eng *= -1

  set_level_false(root_eng, 2)
  common_two = ['to', 'of', 'in', 'is', 'it', 'as', 'on', 'at', 'by']
  for w in common_two:
    set_word_true(root_eng, w)

# ----------------------------------------------------------------------- #
# recursively check whatever trie if the word contains any valid
# words from the selected dictionary.
# valid is a list of all the current words so far.
# ----------------------------------------------------------------------- #

def recurse_check(word, valid, node, prev):
  if (word == ''):
    return
  if (word[0] in node['letters']):
    current_dict = node['letters'][word[0]]
    if (current_dict['is_word'] == True):
      valid.append({'word': prev + word[0], 'prob': current_dict['prob']})
    recurse_check(word[1:], valid, current_dict, prev + word[0])
  else:
    return

# ----------------------------------------------------------------------- #
# recursively look through the word and match the possibilities.
# added is going to be a list of all possible combinations.
# current is going to be the current list being looked at.
# ----------------------------------------------------------------------- #

def recurse_poss(word, poss, added, current):
  if (len(poss) == 0):
    added.append(current)
    return
  for i in range(0, len(poss)):
    ind = string.find(word, poss[i]['word'])
    if (ind >= 0):
      copy = list(current)
      copy.append(poss[i])
      # print copy
      # print poss[i]['word'], len(poss[i]['word']), ind, word[(len(poss[i]['word']) + ind):]
      recurse_poss(word[(len(poss[i]['word']) + ind):], poss[(i + 1):], added, copy)
  added.append(current)
  return

# ----------------------------------------------------------------------- #
# combine possibilities from the english and pinyin lists.
# ----------------------------------------------------------------------- #

def combine_poss(word, eng, pinyin):
  # return list of possibilities in order from beginning to end
  # each element will be dict of 'word': the word, 'type': 'eng' or 'pinyin',
  # and 'index' (indicating the starting index)

  all_ind = []

  prev_word = ''
  curr_word = word
  curr_ind = 0
  for entry in eng:
    w = entry['word']
    ind = string.find(curr_word, w)
    fill = 0    # for use when current word and previous are the same.

    if (w == prev_word):
      ind = string.find(curr_word[len(prev_word):], w)

    curr_ind += ind
    entry['type'] = 'eng'
    entry['ind'] = curr_ind
    all_ind.append(entry)
    curr_word = curr_word[ind:]
    prev_word = w

  curr_word = word
  curr_ind = 0
  prev_word = ''
  for entry in pinyin:
    w = entry['word']
    ind = string.find(curr_word, w)
    fill = 0

    if (w == prev_word):
      fill = len(prev_word)
      ind = string.find(curr_word[fill:], w)

    curr_ind += ind + fill
    entry['type'] = 'pinyin'
    entry['ind'] = curr_ind
    all_ind.append(entry)
    curr_word = curr_word[ind:]
    prev_word = w

  sorted_ind = sorted(all_ind, key=itemgetter('ind'))

  return sorted_ind

# ----------------------------------------------------------------------- #
# look at the combinations possible and rank them by how much of the
# word they encompass.
# ----------------------------------------------------------------------- #
# TODO: get rid of duplicates
def rank_combos(word, valid):
  global shannon_eng
  global shannon_pinyin

  all_val = {}
  word_length = 0

  for c in word:
    if (c.isalpha()):
      word_length += 1

  for i in range(0, len(valid)):
    opt = valid[i]['word']
    ind = valid[i]['ind']
    ans = []
    recurse_poss(word[(ind + len(opt)):], valid[i + 1:], ans, [valid[i]])
    
    # p = one set of possibilities.
    for p in ans:
      poss_length = 0
      prob = 1
      score = 0.0
      entropy = 0
      num_pinyin = 0

      # a = each word in that possibility.
      for a in p:
        # determines which entropy value to use.
        if (a['type'] == 'pinyin'):
          num_pinyin += 1
          entropy = shannon_pinyin
        else:
          entropy = shannon_eng

        poss_length += len(a['word'])

        # scale this according to how many characters it misses afterward?
        # potentially...let's see how it works without.
        indi_score = ((-1.0 * math.log(a['prob'], 2)) / entropy)
        score += indi_score

      skipped = word_length - poss_length
      if (skipped >= (0.5 * word_length)):
        continue 

      # if types are all the same, should be given a higher value.
      if ((num_pinyin == len(p))):
        score /= (1000.0 / ((10 * skipped) + 1))

      # weigh score according to how many characters it skipped.
      score *= math.pow(10, word_length - poss_length)

      # weigh it according to how many words it needs.
      score *= math.pow(10, len(p))

      all_val.setdefault(score, [])
      all_val[score].append(p)
  return all_val

# ----------------------------------------------------------------------- #
# start of the main script.
# ----------------------------------------------------------------------- #

script, filename = sys.argv

load_pinyin_dict()
load_eng_dict()

print 'finished loading dictionaries.'

f = open(filename, 'r')

for check in f.readlines():
  check = check.rstrip()
  check = check.lower()

  valid_pinyin = []
  valid_eng = []
  for i in range(0, len(check)):
    recurse_check(check[i:], valid_pinyin, root_pinyin, '')
  for i in range(0, len(check)):
    recurse_check(check[i:], valid_eng, root_eng, '')

  print '----------- CURRENT PASSWORD: ', check

  # print valid_eng
  # print valid_pinyin

  # find accuracy compositions
  combined_list = combine_poss(check, valid_eng, valid_pinyin)
  # print combined_list
  ranked = rank_combos(check, combined_list)

  max_num = 10
  ind = 0

  prev = ''
  num_eng = 0
  num_pinyin = 0
  valid_length = 0

  for c in check:
    if (c.isalpha()):
      valid_length += 1

  best = []

  # looking at each score
  for key in sorted(ranked.iterkeys()):
    if (ind == max_num):
      break
    num_eng = 0
    num_pinyin = 0
    word_length = 0

    # looking at each set of words for this password.
    for items in ranked[key]:
      curr = '%f: ' % key

      # looking at each word in this set.
      for w in items:
        # figure out types
        if (w['type'] == 'eng'):
          num_eng += 1
        else:
          num_pinyin += 1

        word_length += len(w['word'])
        curr += '(%s, %s) ' % (w['word'], w['type'])

      # gets rid of duplicates (tho...i still don't quite remember why the 
      # duplicates occurred .__.)        
      if (curr != prev):
        ind += 1

        # this is for the number of items it has to be >= to be considered one
        # language or the other.
        num_threshold = 0.6 * len(items)

        # should be checking if enough words match or not. ...should they even
        # be considered in the first place? probably not.
        if (num_eng >= num_threshold):
          best.append({'seq': items, 'score': key, 'type': 'ENGLISH'})
        elif (num_pinyin >= num_threshold):
          best.append({'seq': items, 'score': key, 'type': 'PINYIN'})
        elif ((float(word_length)/valid_length) >= 0.6):
          best.append({'seq': items, 'score': key, 'type': 'HYBRID'})
        else:
          best.append({'seq': items, 'score': key, 'type': 'RANDOM'})
        # sys.stdout.write('%s\n' % curr)
      prev = curr

  if (len(best) > 0):
    prev_score = best[0]['score']
    sys.stdout.write('%f: ' % prev_score)

    for w in best[0]['seq']:
      sys.stdout.write('(%s, %s) ' % (w['word'], w['type']))
    sys.stdout.write('\n')
    sys.stdout.write('%s is a %s password.\n' % (check, best[0]['type']))

    for i in range (1, len(best)):
      curr_score = best[i]['score']
      if (curr_score > (5 * prev_score)):
        break

      sys.stdout.write('%f: ' % curr_score)

      for w in best[i]['seq']:
        sys.stdout.write('(%s, %s) ' % (w['word'], w['type']))
      sys.stdout.write('\n')
      sys.stdout.write('%s is a %s password.\n' % (check, best[i]['type']))

  else:
    sys.stdout.write('%s is a RANDOM password.\n' % check)

  # ranked_pinyin = rank_combos(check, valid_pinyin)
  # for key in sorted(ranked_pinyin.iterkeys()):
  #   print key, ranked_pinyin[key]

  # ranked_eng = rank_combos(check, valid_eng)
  # for key in sorted(ranked_eng.iterkeys()):
  #   print key, ranked_eng[key]