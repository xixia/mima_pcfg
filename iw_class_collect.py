class CollectTerms:

  # initializer
  def __init__(self):
    self.collection = {}

  def add(self, length, word, freq):
    if (len(word) != length):
      return

    self.collection.setdefault(length, {'words': {}, 'total': 0})

    # increment the overall total for this length.
    self.collection[length]['total'] += freq

    self.collection[length]['words'].setdefault(word, {'count': 0, 'prob': 0})
    self.collection[length]['words'][word]['count'] += freq

  def calcProb(self):
    # for each length
    for i in self.collection.keys():
      l = self.collection[i]
      total = l['total']

      for w in l['words'].keys():
        l['words'][w]['prob'] = float(l['words'][w]['count']) / total

  def outputToFile(self, filename):
    self.calcProb()

    # output in order of decreasing probability.
    fo = open(filename + '.txt', 'w')

    # go through each length; sort them by count.
    for i in self.collection.keys():
      l = self.collection[i]
      sorted_prob = sorted(l['words'], key=lambda w: (l['words'][w]['prob']), reverse=True)
      for p in sorted_prob:
        fo.write('%d %s %f\n' % (i, p, l['words'][p]['prob']))

# c = CollectTerms()

# c.add(3, 'hel')
# c.add(4, 'cats')
# c.add(3, 'hel')

# print c.collection
