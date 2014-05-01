import pprint

all_pinyin = [line.rstrip() for line in open('all_pinyin.txt', 'r')]
root = {}
trie_default = {}
trie_default['is_pinyin'] = False
trie_default['letters'] = {}

root = trie_default


for py in all_pinyin:
  current_dict = root
  for c in py:
    trie_default = {}
    trie_default['is_pinyin'] = False
    trie_default['letters'] = {}

    current_dict['letters'].setdefault(c, trie_default)
    current_dict = current_dict['letters'][c]
  current_dict['is_pinyin'] = True

# pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(root)

# open the password list:

passwords = [line.rstrip() for line in open('70yx_cor.txt', 'r')]
total = 0
total_pinyin = 0

pinyin_passwords = []
non_pinyin_passwords = []

for p in passwords:
  found_pinyin = False
  current_dict = root
  i = 0
  current_total = 0
  letters = False

  # print 'checking', p, len(p)

  while i < len(p):
    if (p[i].isalpha()):
      letters = True

    if p[i] in current_dict['letters']:
      current_dict = current_dict['letters'][p[i]]
      current_total += 1
    else:
      # checks if the previous one ended on a correct pinyin.
      if (current_dict['is_pinyin'] == True):
        if (current_total >= 2):
          found_pinyin = True
          current_total = 0
      if (current_dict != root):
        i -= 1
      current_dict = root
      current_total = 0

    i += 1

  if (letters):
    letters = False
    total += 1

  if (found_pinyin):
    total_pinyin += 1
    pinyin_passwords.append(p)
  else:
    non_pinyin_passwords.append(p)

fo_pinyin_yes = open('pinyin_yes.txt', 'w')
fo_pinyin_no = open('pinyin_no.txt', 'w')

for item in pinyin_passwords:
  fo_pinyin_yes.write('%s\n' % item)
fo_pinyin_yes.write(str(total_pinyin/(float(total))))

for item in non_pinyin_passwords:
  fo_pinyin_no.write('%s\n' % item)