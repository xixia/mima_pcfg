import matplotlib.pyplot as plt
from sys import argv

script, gen, jtr = argv

fgen = open(gen, 'r')
fjtr = open(jtr, 'r')

# want to plot y axis as percentage of words that match.
# want to plot x axis as number of guesses made.

# think about the case where one has more guesses made than the other. pad the other.

gen_stat = []
jtr_stat = []
gen_ind = []
jtr_ind = []

ind = 0
gen_stat.append(0)
gen_ind.append(ind)
for line in fgen.readlines():
  ind += 1
  gen_stat.append(float(line))
  gen_ind.append(ind)

print 'done with gen'

ind = 0
jtr_stat.append(0)
jtr_ind.append(ind)
for line in fjtr.readlines():
  ind += 1
  jtr_stat.append(float(line))
  jtr_ind.append(ind)

print 'done with jtr'

num_gen = len(gen_stat)
num_jtr = len(jtr_stat)

cor_ind = gen_ind

if (num_gen > num_jtr):
  diff = num_gen - num_jtr
  last_val = jtr_stat[-1]
  cor_ind = gen_ind
  
  for i in range(0, diff):
    jtr_stat.append(last_val)
# this should almost never happen...
if (num_jtr > num_gen):
  diff = num_jtr - num_gen
  last_val = gen_stat[-1]
  cor_ind = jtr_ind

  for i in range(0, diff):
    gen_stat.append(last_val)

fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.plot(cor_ind, jtr_stat, 'ro', label='john the ripper')
ax1.plot(cor_ind, gen_stat, 'bs', label='pcfg (modified)')
plt.xlabel('number of passwords generated')
plt.ylabel('percentage of passwords in test file cracked')
plt.legend(loc=2)

# plt.plot(num_guessed, percent_correct, 'ro', guessed_new, percent_new, 'bs')
plt.show()