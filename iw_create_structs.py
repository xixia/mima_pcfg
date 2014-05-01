import operator
import sys

script, filename, outname = sys.argv

files = ['70yx_cor.txt', 'uuu9_cor.txt', 'csdn_cor.txt']
file_test = ['myspace_cor.txt']

# f_output = open('struc.txt', 'w')
f = open(filename, 'r')
fo = open(outname + '.txt', 'w')

# potential states = 'c' for character, 'd' for digit, and 's' for special char
g_structs = {}
g_prob = {}
prev_state = ''
total = 0
total_lines = 0

for l in f.readlines():
  current_struct = ''
  prev_state = ''
  total = 0

  # examine each character in the string.
  for c in l:
    if (c == '\n'):
      current_struct += prev_state + str(total)
      break
    curr_state = ''
    if (c.isdigit()):
      curr_state = 'n'
    elif (c.isalpha()):
      curr_state = 'c'
    else:
      curr_state = 's'

    if ((curr_state != prev_state) and (prev_state != '')):
      current_struct += prev_state + str(total)
      total = 0

    prev_state = curr_state
    total += 1

  g_structs.setdefault(current_struct, 0)
  g_structs[current_struct] += 1
  total_lines += 1

for s in g_structs.keys():
  g_prob[s] = float(g_structs[s] / float(total_lines))

sorted_prob = sorted(g_prob.iteritems(), key=operator.itemgetter(1), reverse=True)
for p in sorted_prob:
  fo.write('%s %f\n' % (p[0], p[1]))