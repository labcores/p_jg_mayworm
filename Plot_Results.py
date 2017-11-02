import numpy as np
from matplotlib import pyplot as plt

from scipy.stats import pearsonr


#------------------------------------------------------------------------------#
def get_arrays_means(arrays):
    lists = []
    means = []
    return lists


#------------------------------------------------------------------------------#

f = open("no_similarity.csv")
matrix = []

for line in f:
    vec = line.split(';')
    vec = [float(x) for x in vec]
    matrix.append(vec)

a = np.array(matrix)
a = a.T

steps, agents, encounters, exchanges, times, precision, recall = np.array_split(a, 7)

step_t = [np.mean(x) for x in steps]
mean_agents = [np.mean(x) for x in agents]
mean_encounters = [np.mean(x) for x in encounters]
mean_exchanges = [np.mean(x) for x in exchanges]
mean_times = [np.mean(x) for x in times]
mean_precision = [np.mean(x) for x in precision]
mean_recall = [np.mean(x) for x in recall]


ax = np.multiply(mean_precision, mean_recall)
bx = np.add(mean_precision, mean_recall)
cx = np.divide(ax, bx)
f_score = 2 *  cx

#------------------------------------------------------------------------------#

f2 = open("ed_similarity.csv")
matrix2 = []

for line in f2:
    vec = line.split(';')
    vec = [float(x) for x in vec]
    matrix2.append(vec)

a2 = np.array(matrix2)
a2 = a2.T

aux1, aux2, aux3, ed_exchanges, ed_times, ed_precision, ed_recall = np.array_split(a2, 7)

mean_ed_exchanges = [np.mean(x) for x in ed_exchanges]
mean_ed_times = [np.mean(x) for x in ed_times]
mean_ed_precision = [np.mean(x) for x in ed_precision]
mean_ed_recall = [np.mean(x) for x in ed_recall]

eax = np.multiply(mean_ed_precision, mean_ed_recall)
ebx = np.add(mean_ed_precision, mean_ed_recall)
ecx = np.divide(eax, ebx)
f_score_ed = 2 * ecx

#------------------------------------------------------------------------------#

f3 = open("ds_similarity.csv")
matrix3 = []

for line in f3:
    vec = line.split(';')
    vec = [float(x) for x in vec]
    matrix3.append(vec)

a3 = np.array(matrix3)
a3 = a3.T
aux1, aux2, aux3, ds_exchanges, ds_times, ds_precision, ds_recall = np.array_split(a3, 7)

mean_ds_exchanges = [np.mean(x) for x in ds_exchanges]
mean_ds_times = [np.mean(x) for x in ds_times]
mean_ds_precision = [np.mean(x) for x in ds_precision]
mean_ds_recall = [np.mean(x) for x in ds_recall]

f_score_ds = 2 * np.divide(np.multiply(mean_ds_precision, mean_ds_recall), np.add(mean_ds_precision, mean_ds_recall))

split = 9

#--- Exchanges --------------------------------------------------------#
plt.figure(1)
ax = plt.subplot(111)

ax.errorbar(step_t[::split], mean_exchanges[::split], \
    fmt = ':p', label = 'NSS', color = 'darkorange', linewidth = 3.0, alpha = 0.9, ms = 10.0, mfc = 'orangered')

ax.errorbar(step_t[::split], mean_ed_exchanges[::split], \
    fmt = '--H', label = 'EDS', color = 'darkcyan', linewidth = 3.0, alpha = 0.7, ms = 10.0, mfc = 'teal')

ax.errorbar(step_t[::split], mean_ds_exchanges[::split], \
    fmt = '-o', label = 'DDS', color = 'darkblue', linewidth = 3.0, alpha = 0.7, ms = 9.0)

ax.set_xlabel('Steps')
ax.set_ylabel('Exchanges')

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.13),
          fancybox=False, shadow=False, ncol=5)

#--- Precision ----------------------------------------------------------------#

plt.figure(2)
ax = plt.subplot(111)

ax.errorbar(step_t[::split], mean_precision[::split], \
    fmt = ':p', label = 'NSS', color = 'darkorange', linewidth = 3.0, alpha = 0.9, ms = 10.0, mfc = 'orangered')

ax.errorbar(step_t[::split], mean_ed_precision[::split], \
    fmt = '--H', label = 'EDS', color = 'darkcyan', linewidth = 3.0, alpha = 0.7, ms = 10.0, mfc = 'teal')

ax.errorbar(step_t[::split], mean_ds_precision[::split], \
    fmt = '-o', label = 'DDS', color = 'darkblue', linewidth = 3.0, alpha = 0.7, ms = 9.0)

ax.set_xlabel('Steps')
ax.set_ylabel('Precision')

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.13),
          fancybox=False, shadow=False, ncol=5)

#--- Recall -------------------------------------------------------------------#

plt.figure(3)
ax = plt.subplot(111)
ax.errorbar(step_t[::split], mean_recall[::split], \
    fmt = ':p', label = 'NSS', color = 'darkorange', linewidth = 3.0, alpha = 0.9, ms = 10.0, mfc = 'orangered')

ax.errorbar(step_t[::split], mean_ed_recall[::split], \
    fmt = '--H', label = 'EDS', color = 'darkcyan', linewidth = 3.0, alpha = 0.7, ms = 10.0, mfc = 'teal')

ax.errorbar(step_t[::split], mean_ds_recall[::split], \
    fmt = '-o', label = 'DDS', color = 'darkblue', linewidth = 3.0, alpha = 0.7, ms = 9.0)

ax.set_xlabel('Steps')
ax.set_ylabel('Recall')

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.13),
          fancybox=False, shadow=False, ncol=5)

#--- F-Score ------------------------------------------------------------------#

plt.figure(4)
ax = plt.subplot(111)
ax.errorbar(step_t[::split], f_score[::split], \
    fmt = ':p', label = 'NSS', color = 'darkorange', linewidth = 3.0, alpha = 0.9, ms = 10.0, mfc = 'orangered')

ax.errorbar(step_t[::split], f_score_ed[::split], \
    fmt = '--H', label = 'EDS', color = 'darkcyan', linewidth = 3.0, alpha = 0.7, ms = 10.0, mfc = 'teal')

ax.errorbar(step_t[::split], f_score_ds[::split], \
    fmt = '-o', label = 'DDS', color = 'darkblue', linewidth = 3.0, alpha = 0.7, ms = 9.0)

ax.set_xlabel('Steps')
ax.set_ylabel('F_Score')

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.13),
          fancybox=False, shadow=False, ncol=5)

#--- Exec-Times ---------------------------------------------------------------#
# split  = 9
N = len(mean_encounters[10::split])
ind = np.arange(N)  # the x locations for the groups
width = 0.27       # the width of the bars

fig = plt.figure(5)
ax = fig.add_subplot(111)

rects1 = ax.bar(ind, mean_times[10::split], width, color='darkorange', alpha = 0.9)
rects2 = ax.bar(ind+width, mean_ed_times[10::split], width, color='teal', alpha = 0.8)
rects3 = ax.bar(ind+width*2, mean_ds_times[10::split], width, color='darkblue', alpha = 0.8)

ax.set_xticklabels([int(mean) for mean in mean_encounters[10::split]])#('0', '20', '40', '60', '80', '100', '120'))
ax.set_ylabel('Execution Times')
ax.set_xlabel('Encounters')
ax.set_xticks(ind+width)

ax.legend((rects1[0], rects2[0], rects3[0]), ('NSS', 'EDS', 'DSS'))

#------------------------------------------------------------------------------#

plt.tight_layout()
plt.show()

#--- Plotting Map -------------------------------------------------------------#

# sf = shp.Reader(file_path)
# for shape in sf.shapeRecords():
#     x = [i[0] for i in shape.shape.points[:]]
#     y = [i[1] for i in shape.shape.points[:]]
#     ax4.plot(x, y, color= 'gray', linewidth = '0.5')

# ax4.plot([loc[0] for loc in sim.arrival_locations], [loc[1] for loc in sim.arrival_locations], 'ro', 
#                                                                 label = 'Arrivals', alpha = .5, ms = 10)

# ax4.plot([loc[0] for loc in sim.target_locations], [loc[1] for loc in sim.target_locations], 'bo', 
#                                                         label = 'Destinations', alpha = .5, ms = 5)

# ax4.plot([agent.path[0][0] for agent in sim.agents_list], [agent.path[0][1] for agent in sim.agents_list], 'go', 
#                                                         label = 'Agents', alpha = .5, ms = 2)

#--- Plotting Graph -----------------------------------------------------------#

# for i in sim.graph.nodes():
#   print i
# pos = {xy: xy for xy in sim.graph.nodes()}
# nx.draw_networkx_nodes(sim.graph, pos, node_size = 15, node_color = 'b')
# nx.draw_networkx_edges(sim.graph, pos, edge_color = 'k')

# plt.axis('equal')
# plt.show()