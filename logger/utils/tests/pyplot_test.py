import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot
from matplotlib.dates import DateFormatter



pyplot.scatter([x / 2.0 for x in range(10)], [(x / 2.0) ** 2 for x in range(10)],
               color = 'blue', marker = 'D', s = 30)
pyplot.xlabel('coordonnee X')
pyplot.ylabel('coordonnee Y')
pyplot.title('mon titre')
pyplot.text(0, 20, 'parabole')
pyplot.annotate('annotation', xy = (0, 0), xytext = (1, 10),
                arrowprops = {'facecolor': 'red', 'shrink': 0.1})
pyplot.grid()
pyplot.show()
