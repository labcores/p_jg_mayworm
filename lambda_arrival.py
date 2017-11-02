  
import numpy as np
from matplotlib import pyplot as plt 

def morning_distrib(step):
	return  1 / (1 + np.exp(step/200.0))

def evening_distrib(step):
	return  1 / (1 + np.exp(-step/200.0)) #return  1 / (1 + (np.exp(-step)/30) * 50) + 2

steps = 1000

phase_1 = [morning_distrib(x) for x in xrange(steps)]
phase_2 = [evening_distrib(x) for x in xrange(steps)]

fig = plt.figure(figsize=(8.0, 4.0))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)


ax1.plot([x for x in xrange(steps)], phase_1, color = 'darkblue', linewidth = 2.0, alpha = 0.8)
ax2.plot([x for x in xrange(steps)], phase_2, color = 'darkblue', linewidth = 2.0, alpha = 0.8)

ax1.set_title('Morning Distribution')
ax1.legend(loc='best')

ax2.set_title('Afternoon Distribution')
ax2.legend(loc='best')

fig.text(0.5, 0.001, 'x', ha='center', fontsize = 14)
fig.text(0.001, 0.5, 'f(x)', va='center', rotation='vertical',fontsize = 12)

plt.tight_layout()
plt.show()
