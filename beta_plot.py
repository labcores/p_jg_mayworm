import numpy as np
from matplotlib import pyplot as plt

def p(alfa,beta):
	data = np.random.beta(alfa, beta, 1000)
	values, base  = np.histogram(data, bins=40)
	cumulative = np.cumsum(values)
	return base, cumulative


hi1, hi2 = p(1.0, 5.0)
med1, med2 = p(2.0, 2.0)
low1, low2 = p(7.0, 1.0)

fig = plt.figure(figsize=(8.5, 4.0))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

ax1.plot(hi1[:-1], hi2, color = 'darkblue', linewidth = 2.0, alpha = 0.8)
ax2.plot(med1[:-1], med2, color = 'darkblue', linewidth = 2.0, alpha = 0.8)
ax3.plot(low1[:-1], low2, color = 'darkblue', linewidth = 2.0, alpha = 0.8)

ax1.set_title('alpha = 1, beta = 5', fontsize = 10.5)
ax2.set_title('alpha = 2, beta = 2', fontsize = 10.5)
ax3.set_title('alpha = 5, beta = 1', fontsize = 10.5)

fig.text(0.5, 0.001, 'x', ha='center', fontsize = 14)
fig.text(0.004, 0.5, 'beta(x, alpha, Beta)', va='center', rotation='vertical',fontsize = 12)

plt.tight_layout()
plt.show()
