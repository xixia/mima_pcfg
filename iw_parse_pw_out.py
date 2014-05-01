from random import shuffle

# f_myspace = open('myspace.txt', 'r')
# fo_myspace = open('myspace_cor.txt', 'w')

# lines = f_myspace.readlines()
# shuffle(lines)

# for i in range(0,1000):
#   fo_myspace.write(lines[i])

# ------------------------------------------------------------------- #
# 70yx parsing.

f_70yx = open('70yx.txt', 'r')
fo_70yx = open('70yx_cor.txt', 'w')

all_pw = []

for line in f_70yx.readlines():
  l_split = line.split()
  all_pw.append(l_split[2].rstrip())

all_pw = set(all_pw)
passwords = list(all_pw)
shuffle(passwords)

for pw in passwords:
  fo_70yx.write('%s\n' % pw)

# for i in range(0,500000):
#   l_split = lines[i].split()
#   fo_70yx.write('%s\n' % l_split[2])

# ------------------------------------------------------------------- #
# csdn parsing.

# f_csdn = open('csdn_samp.txt', 'r')
# fo_csdn = open('csdn_cor.txt', 'w')

# lines = f_csdn.readlines()
# shuffle(lines)

# for line in lines:
#   l_split = line.split(' # ')
#   fo_csdn.write(l_split[1])
#   fo_csdn.write('\n')

# ------------------------------------------------------------------- #
# uuu9 parsing.

# f_uuu9 = open('uuu9_samp.txt', 'r')
# fo_uuu9 = open('uuu9_cor.txt', 'w')

# lines = f_uuu9.readlines()
# shuffle(lines)

# for line in lines:
#   l_split = line.split()
#   fo_uuu9.write(l_split[1])
#   fo_uuu9.write('\n')

# ------------------------------------------------------------------- #
# print a sample of 200 words from a specified list.

# f_list = open('70yx.txt', 'r')
# fo_list = open('70yx_samp.txt', 'w')

# lines = f_list.readlines()
# shuffle(lines)

# for i in range(0,200):
#   l_split = lines[i].split()
#   fo_list.write('%s\n' % l_split[2])

# ------------------------------------------------------------------- #
# print a sample of 200 words that are mostly letters from a specified
# list.

# f_list = open('70yx.txt', 'r')
# fo_list = open('70yx_samp.txt', 'w')

# lines = f_list.readlines()
# shuffle(lines)

# i = 0
# j = 0
# while (i < 200):
#   l_split = lines[j].split()
#   j += 1

#   num_alph = 0
#   for c in l_split[2]:
#     if (c.isalpha()):
#       num_alph += 1
#   print num_alph

#   if (num_alph >= (len(l_split[2]) * 0.5)) or (num_alph >= 5):
#     fo_list.write('%s\n' % l_split[2])
#     print l_split[2]
#     i += 1
