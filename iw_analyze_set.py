# USAGE: python iw_analyze_set.py [filename of passwords to analyze] [prefix to use for output files]

import operator
import string
import sys
import math

from iw_class_collect import CollectTerms

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

def recurse_poss(word, poss, added, current, curr_ind):
  if (len(poss) == 0):
    added.append(current)
    # print 'ADDING ', current
    return

  # print word, poss, current, curr_ind

  for i in range(0, len(poss)):
    if (poss[i]['ind'] >= curr_ind):
      ind = string.find(word, poss[i]['word'])
      if (ind >= 0):
        copy = list(current)
        copy.append(poss[i])
        # print copy
        # print poss[i]['word'], len(poss[i]['word']), ind, word[(len(poss[i]['word']) + ind):]
        next_ind = len(poss[i]['word']) + ind
        recurse_poss(word[next_ind:], poss[(i + 1):], added, copy, next_ind + curr_ind)

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
      same = True
      for i in range(1, len(w)):
        if w[i] != w[i - 1]:
          same = False
          break
      if not same:
        fill = len(prev_word)
        curr_word = curr_word[fill:]
        ind = string.find(curr_word, w)
      else:
        fill = 1
        curr_word = curr_word[fill:]
        ind = string.find(curr_word, w)

    curr_ind += ind + fill
    entry['type'] = 'eng'
    entry['ind'] = curr_ind
    # print w, curr_ind, ind, curr_word
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
      same = True
      for i in range(1, len(w)):
        if w[i] != w[i - 1]:
          same = False
          break
      if not same:
        fill = len(prev_word)
        curr_word = curr_word[fill:]
        ind = string.find(curr_word, w)
      else:
        fill = 1
        curr_word = curr_word[fill:]
        ind = string.find(curr_word, w)

    curr_ind += ind + fill
    entry['type'] = 'pinyin'
    entry['ind'] = curr_ind
    all_ind.append(entry)
    curr_word = curr_word[ind:]
    prev_word = w

  sorted_ind = sorted(all_ind, key=operator.itemgetter('ind'))

  return sorted_ind

# ----------------------------------------------------------------------- #
# look at the combinations possible and rank them by how much of the
# word they encompass.
# ----------------------------------------------------------------------- #
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
    curr_ind = ind + len(opt)
    recurse_poss(word[curr_ind:], valid[i + 1:], ans, [valid[i]], curr_ind)

    # print ans
    
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
      if ((num_pinyin == len(p)) or (num_pinyin == 0)):
        score /= (1000.0 / ((10 * skipped) + 1))

      # weigh score according to how many characters it skipped.
      score *= math.pow(10, skipped)

      # weigh it according to how many words it needs. only if there are characters skipped.
      if (skipped != 0):
        score *= math.pow(10, len(p) - 1)

      all_val.setdefault(score, [])
      all_val[score].append(p)
  return all_val

# ----------------------------------------------------------------------- #
# start of the main script. (massive...def need to modularize).
# ----------------------------------------------------------------------- #

script, filename, prefix = sys.argv

load_pinyin_dict()
load_eng_dict()

print 'finished loading dictionaries.'

f = open(filename, 'r')
fo = open(prefix + '_types.txt', 'w')
fo_struct = open(prefix + '_structs.txt', 'w')

# maintains the structures' probabilities.
g_prob = {}

# maintains the total number of passwords.
total_lines = 0

# maintain all of the structures (corrected)
structs_corr = {}

# all of these will be of the format: num_str[length] = {'words': {word: number}, 'total': number}
num_str = CollectTerms()
spec_str = CollectTerms()
pinyin_str = CollectTerms()
eng_str = CollectTerms()
rand_str = CollectTerms()

total_pinyin = 0
total_nonnum = 0

types = ['ENGLISH', 'PINYIN', 'RANDOM', 'HYBRID']

for line in f.readlines():
  line = line.rsplit(' ', 1)
  check = line[0]
  freq = int(line[1])

  # print check

  if ((total_lines % 1000) == 0):
    print 'on password', total_lines

  # analyze the structure of the password.
  current_struct = ''
  prev_state = ''
  total = 0         # used for determining the struct.

  # other needed variables.
  max_num = 10      # TODO: figure out what this is...?
  valid_length = 0  # valid length = length of just characters in password.

  # examine each character in the string. determines the 'general' structure here.
  # should probably have the structure analysis at the bottom. doesn't matter if have
  # to iterate through the characters twice right?
  comp = []         # list of grammar components.
  ind = 0           # starting index of this component.
  prev = ''         # keeps track of the previous character.
  same = 0          # keeps track of the longest string of same characters.
  flag_ident = False  # flag which notes if this password is just a string of identical characters.
  letters = {}      # dictionary to keep track of the letters in this password.

  # determines the primitive structure of this passwords (letters v. numbers v. special)
  for c in check:
    curr_state = ''
    if (c.isdigit()):
      curr_state = 'n'
    elif (c.isalpha()):
      curr_state = 'c'
      valid_length += 1

      # put this letter in the dictionary.
      letters.setdefault(c, 0)
      letters[c] += 1

      # should only do this check when they're characters.
      if (c == prev):
        same += 1
      prev = c

    else:
      curr_state = 's'

    if ((curr_state != prev_state) and (prev_state != '')):
      current_struct += prev_state + str(total)
      comp.append({'type': prev_state, 'len': total, 'ind': (ind - total)})
      total = 0
    ind += 1

    prev_state = curr_state
    total += 1

  current_struct += prev_state + str(total)
  comp.append({'type': prev_state, 'len': total, 'ind': (ind - total)})

  if (len(letters) < (0.3 * valid_length)):
    flag_ident = True

  if (same >= (0.7 * len(check))):
    flag_ident = True

  # completed primitive structure determining at this point. onto analysis!
  total_lines += freq

  # ----------------------------------------------------------------------- #

  # analyze the language of the password.
  valid_pinyin = []
  valid_eng = []
  best = []
  
  if (not flag_ident):
    for i in range(0, len(check)):
      recurse_check(check[i:], valid_pinyin, root_pinyin, '')
    for i in range(0, len(check)):
      recurse_check(check[i:], valid_eng, root_eng, '')

    if (len(valid_pinyin) != 0) and (len(valid_eng) != 0):
      total_nonnum += freq

    fo.write('----------- CURRENT PASSWORD: %s\n' % check)

    # find accuracy compositions
    combined_list = combine_poss(check, valid_eng, valid_pinyin)
    ranked = rank_combos(check, combined_list)

    # looking at each score - analyze if it's overall pinyin or english.
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

  # need logic on constructing the grammar structures...!
  best_opt = []
  comp_correct = []

  if (len(best) > 0):
    best_opt = list(best[0]['seq'])
  
  # print comp
  for part in comp:
    t = part['type']
    l = part['len']
    i = part['ind']

    # i have type, len, and ind for each part.

    # case if it's a number.
    if (t == 'n'):
      num_str.add(l, check[i:(i + l)], freq)
      comp_correct.append(t + str(l))

    # case if it's a special character.
    elif (t == 's'):
      spec_str.add(l, check[i:(i + l)], freq)
      comp_correct.append(t + str(l))

    # case if it's a character.
    elif (t == 'c'):
      max_ind = i + l

      # check every word in best option
      for w in best_opt:
        # each word has a type, word, and ind
        if ((w['ind'] < max_ind) and (w['ind'] >= i)):
          # check if there are characters before this word that 
          # aren't accounted for.
          skipped = w['ind'] - i
          if (skipped != 0):
            rand_str.add(skipped, check[i:w['ind']], freq)
            comp_correct.append('r' + str(skipped))

          wlen = len(w['word'])
          if (w['type'] == 'pinyin'):
            pinyin_str.add(wlen, w['word'], freq)
            comp_correct.append('p' + str(wlen))
          else:
            eng_str.add(wlen, w['word'], freq)
            comp_correct.append('e' + str(wlen))
          i = w['ind'] + wlen
        else:
          break

      # check if there's leftovers that the words didn't catch.
      if ((max_ind - i) != 0):
        if (max_ind < i):
          print max_ind, i, comp_correct, check
        rand_str.add(max_ind - i, check[i:max_ind], freq)
        comp_correct.append('r' + str(max_ind - i))

  # create the modified structure.
  struct = ''.join(comp_correct)
  structs_corr.setdefault(struct, {'count': 0, 'prob': 0})
  structs_corr[struct]['count'] += freq

  # outputs the type for error checking, basically.
  if (len(best) > 0):
    prev_score = best[0]['score']
    fo.write('%f: ' % prev_score)

    for w in best[0]['seq']:
      fo.write('(%s, %s) ' % (w['word'], w['type']))
    fo.write('\n')
    fo.write('%s is a %s password.\n' % (check, best[0]['type']))

    if (best[0]['type'] == 'PINYIN'):
      total_pinyin += freq

    # for i in range (1, len(best)):
    #   curr_score = best[i]['score']
    #   if (curr_score > (5 * prev_score)):
    #     break

    #   fo.write('%f: ' % curr_score)

    #   for w in best[i]['seq']:
    #     fo.write('(%s, %s) ' % (w['word'], w['type']))
    #   fo.write('\n')
    #   fo.write('%s is a %s password.\n' % (check, best[i]['type']))

  else:
    fo.write('%s is a RANDOM password.\n' % check)

# calculate probabilities:
for s in structs_corr.keys():
  structs_corr[s]['prob'] = float(structs_corr[s]['count'])/total_lines

# finallyyyy.
sorted_prob = sorted(structs_corr, key=lambda s: (structs_corr[s]['prob']), reverse=True)
for p in sorted_prob:
  fo_struct.write('%s %f\n' % (p, structs_corr[p]['prob']))

num_str.outputToFile(prefix + '_num')
pinyin_str.outputToFile(prefix + '_pinyin')
eng_str.outputToFile(prefix + '_eng')
rand_str.outputToFile(prefix + '_rand')
spec_str.outputToFile(prefix + '_spec')

print total_pinyin
print float(total_pinyin) / total_lines
print float(total_pinyin) / total_nonnum
print total_lines, total_nonnum