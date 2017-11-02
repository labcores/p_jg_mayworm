#!/usr/bin/python
# -*- coding: utf-8 -*-

import thread
import threading
import numpy as np
import random as rd
import shapefile as shp
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter


#------------------------------------------------------------------------------#

from Simulation import Simulation

#--- Setting Locations --------------------------------------------------------#


#Major Starting Points: Proximities of Aeroporto Santos Dummont and Central do Brasil
airport = [(-43.1694, -22.9098)]
bus_terminal = [(-43.193306, -22.902198)]

# List of Subway Stations:
# 1) Central
# 2) Presidente Vargas
# 3) Estação Uruguaiana
# 4) Carioca
# 5) Cinelândia
subway_stations = [(-43.190937, -22.905023),
                   (-43.186056, -22.903254),
                   (-43.181490, -22.902939),
                   (-43.17795,  -22.907480),
                   (-43.175579, -22.911522)]

# List of alternative spawn locations:
# 1) Av. Rio Branco
# 2) Av. Mem de Sa
# 3) Praça da Cruz Vermelha
# 4) Rua da Carioca
# 5) Rua Riachuelo
street_locations = [(-43.178079, -22.903910),
                    (-43.184939, -22.912549),
                    (-43.188276, -22.911966),
                    (-43.180278, -22.906647),
                    (-43.180278, -22.906647)]

key_locations = [(-43.167504, -22.911158), 
                 (-43.193306, -22.902198),
                 (-43.190937, -22.905023),
                 (-43.186056, -22.903254),
                 (-43.181490, -22.902939),
                 (-43.17795,  -22.907480),
                 (-43.175579, -22.911522),
                 (-43.190937, -22.905023),
                 (-43.186056, -22.903254),
                 (-43.181490, -22.902939),
                 (-43.17795,  -22.907480),
                 (-43.175579, -22.911522)]
                 
locations_probs = [4, 3, 2, 1] # Spanw probabilities for key locations

#--- Setting an interests list ------------------------------------------------#

items_list = [
             "Abdominal Radiology",
             "Addiction Psychiatry",
             "Adolescent Medicine Pediatrics",
             "Adult Reconstructive Orthopedics",
             "Advanced Heart Failure & Transplant",
             "Allergy & Immunology",
             "Cardiothoracic Radiology",
             "Cardiovascular Disease",
             "Chemical Pathology",
             "Child & Adolescent Psychiatry",
             "Child Neurology",
             "Clinical & Laboratory Immunology",
             "Clinical Cardiac Electrophysiology",
             "Clinical Neurophysiology",
             "Colon & Rectal Surgery",
             "Congenital Cardiac Surgery",
             "Craniofacial Surgery",
             "Critical Care Medicine Anesthesiology",
             "Critical Care Medicine Internal Medicine",
             "Cytopathology Pathology-Anatomic & Clinical",
             "Dermatology",
             "Dermatopathology"
             ]

#Creating a simple docs list to be exchanged in the simulation
doc_list = rd.sample(xrange(1, 200), 199)

#Setting document's classifications
split_docs = np.array_split(doc_list, len(items_list))
doc_classes = dict.fromkeys(items_list)

for key in doc_classes.keys():
    doc_classes[key] = rd.choice(split_docs)


#Setting time conversion: seconds to step
def time_conversion(seconds):
    steps = seconds / 0.766666667
    return int(steps)

def run_experiments(file, obj, rounds, cmd_string):
    for n in xrange(rounds):
        obj.run(n, cmd_string)
        print 
        step_t, num_agents, num_encounters, num_exchanges, times, precision, recall = obj.get_data()
        lists = step_t + num_agents + num_encounters + num_exchanges + times + precision + recall

        file.write(";".join([str(x) for x in lists]) + '\n') 
        obj.reset()
    file.close()

#--- Setting simulation -------------------------------------------------------#
rounds = 30
seconds = 100
file_path = "RJ_Center_Map/walkways.shp"
sim = Simulation(file_path, key_locations, locations_probs, time_conversion(seconds), items_list, doc_list, doc_classes)
print "\n#--- Initializing Simulation ---#\n"

#--- Running Experiments ------------------------------------------------------#
file_data_1 = open('no_similarity.csv','w') 
print '--> No Similarity\n'

for n in xrange(rounds):
    sim.run(n, 'no_similarity')
    step_t, num_agents, num_encounters, num_exchanges, times, precision, recall = sim.get_data()
    lists = step_t + num_agents + num_encounters + num_exchanges + times + precision + recall

    file_data_1.write(";".join([str(x) for x in lists]) + '\n') 
    sim.reset()
file_data_1.close()

#------------------------------------------------------------------------------#

file_data_2 = open('ed_similarity.csv','w') 
print '--> Euclidean Distance Similarity\n'

for n in xrange(rounds):
    sim.run(n, 'ed_similarity')
    step_t, num_agents, num_encounters, num_exchanges, times, precision, recall = sim.get_data()
    lists = step_t + num_agents + num_encounters + num_exchanges + times + precision + recall

    file_data_2.write(";".join([str(x) for x in lists]) + '\n') 
    sim.reset()
file_data_2.close()


#------------------------------------------------------------------------------#

file_data_3 = open('ds_similarity.csv','w') 
print '--> Dempster Shafer Similarity\n'

for n in xrange(rounds):
    sim.run(n, 'ds_similarity')
    step_t, num_agents, num_encounters, num_exchanges, times, precision, recall = sim.get_data()
    lists = step_t + num_agents + num_encounters + num_exchanges + times + precision + recall

    file_data_3.write(";".join([str(x) for x in lists]) + '\n') 
    sim.reset()
file_data_3.close()

#==============================================================================#


