#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

import sys
import random as rd
import numpy as np
import networkx as nx
from haversine import haversine


#------------------------------------------------------------------------------#

from Agent import Agent
import Geo

#------------------------------------------------------------------------------#

#==============================================================================#
#--- Class: Simulation --------------------------------------------------------#
#==============================================================================#

class Simulation(object):

    def __init__(self, file_path, key_locations, location_probabilities, duration = 120, interests = [], documents = [], classifications = {}):
        self.graph = self.generate_graph(file_path) 
        self.doc_classes = classifications
        self.arrival_locations = self.set_valid_locations(key_locations, 0.05)
        self.target_locations = self.set_valid_locations(self.arrival_locations, 0.7)
        self.arrival_probs = location_probabilities
        self.all_interests = interests
        self.all_documents = documents
        self.agents_list = []
        self.duration = duration # Number of seconds in a day: 86400
        self.n_arrivals = 0

       #--- Statistical Data ---#
        self.steps = []
        self.num_agents = []
        self.agent_departures = []
        self.num_departures = []
        self.precision = []
        self.recall = []

        # No Similarity
        self.num_encounters = []
        self.num_exchanges = []
        self.exec_times = []
        
#------------------------------------------------------------------------------#

    def get_agents(self):
        return self.agents_list
    
#------------------------------------------------------------------------------#

    def get_data(self):
        return self.steps, self.num_agents, \
        self.num_encounters, self.num_exchanges, self.exec_times, \
        self.precision, self.recall
         
#------------------------------------------------------------------------------#

    def get_precision(self, agent):
        correct_docs = 0
        total = 0
        for interest in agent.interests:
            if interest[0] in agent.documents.keys():

                agent_docs = agent.documents[interest[0]]
                all_docs = self.doc_classes[interest[0]]

                correct_docs += len(list(set(agent_docs).intersection(all_docs)))
                total += len(agent.documents[interest[0]])

        if total > 0:
            return correct_docs/total
        else:
            return 0

#------------------------------------------------------------------------------#

    def get_recall(self, agent):
        count = 0
        total = 0
        for interest in agent.interests:
            if interest[0] in agent.documents.keys():
                count += len(agent.documents[interest[0]]) 
                total += len(self.doc_classes[interest[0]])

        if total > 0:
            return count/total
        else:
            return 0

#------------------------------------------------------------------------------#

    def get_path_len(self, path):
        total_lengh = 0
        for idx, coord in enumerate(path):
            next_coord = path[(idx + 1) % len(path)]

            total_lengh += haversine(coord, next_coord) 
        return total_lengh

#------------------------------------------------------------------------------#

    # Calculating random spawn points in 80 meter radius around a given location(lat/lng)
    def get_perimeter_coords(self, location, locations_list, radius):
        proximity_coords = []
        for i in locations_list:
            if i != location:
                if haversine((location[0], location[1]), (i[0], i[1])) <= radius:
                    proximity_coords.append((i[0], i[1]))
        return proximity_coords

#------------------------------------------------------------------------------#

    def set_valid_locations(self, key_locations, distance):
        near = []
        valid_locs = []
        for loc in key_locations:
            near = self.get_perimeter_coords(loc, self.graph.nodes(), distance)
            valid_locs += near
        return valid_locs

#==============================================================================#

    # This function reads the shp file and returns the biggest connected component of the generated graph
    def generate_graph(self, file_path):
        graph = nx.read_shp(file_path)
        components_list = sorted(nx.connected_components(graph.to_undirected()), key=len, reverse=True)
        subgraph = graph.subgraph(components_list[0]) # Biggest component is always in the first position
        return subgraph.to_undirected()

#------------------------------------------------------------------------------#

    def morning_distrib(self, step):
        return  1 / (1 + np.exp(-step))

    def evening_distrib(self, step):
        return  1 / (1 + np.exp(-step)) #return  1 / (1 + (np.exp(-step)/30) * 50) + 2

#------------------------------------------------------------------------------#

    def day_periods(self, step):

        if step < (self.duration / 2):
            return self.morning_distrib(step)
        else:
            return self.evening_distrib(step) 

#------------------------------------------------------------------------------#

    def create_arrivals(self, lam, ratio = 0.013):
        x = np.random.uniform(0, 1)

        if x > ratio:
            self.n_arrivals = np.random.poisson(lam)
            aux = self.n_arrivals
            self.n_arrivals = 0
            return aux

        else:
            self.n_arrivals += np.random.poisson(lam)
            return 0

#------------------------------------------------------------------------------#

    def generate_arrivals(self, step):
        num_arrival_points = len(self.arrival_locations)
        num_target_points = len(self.target_locations)

        num_arrivals = self.create_arrivals(self.day_periods(step))
        
        pos_arrival = np.random.choice(num_arrival_points, num_arrivals, self.arrival_probs)
        pos_target = np.random.choice(num_target_points, num_arrivals)

        found = False
        try:
            for i in xrange(num_arrivals):
                if pos_arrival.size and pos_target.size:
                    start_pos = rd.choice(pos_arrival) # pos_arrival[i]
                    dest_pos =  rd.choice(pos_target) # pos_target[i]
                    start = self.arrival_locations[start_pos]
                    dest = self.target_locations[dest_pos]
                    
                    if start != dest:
                        path = nx.astar_path(self.graph, source = start, target = dest) #rd.choice([p for p in nx.all_shortest_paths(self.graph, source = start, target = dest)])
                        agent = Agent(path, self.all_interests, self.all_documents, self.doc_classes)
                        self.agents_list.append(agent)
                
        except nx.NetworkXNoPath:
            print "No path between points \n"
            pass

#------------------------------------------------------------------------------#

    def generate_departures(self):
        for agent in self.agents_list:
            if agent.finished_path == False and agent.pos == agent.path[len(agent.path)-1]:
                start = agent.pos
                dest = agent.path[0]
                path = nx.astar_path(self.graph, source = start, target = dest) #rd.choice([p for p in nx.all_shortest_paths(self.graph, source = start, target = dest)])
                new_agent = Agent(path, self.all_interests, self.all_documents, self.doc_classes, True)
                self.agents_list.append(new_agent)
                self.agents_list.remove(agent)

            elif agent.finished_path == True and agent.pos == agent.path[len(agent.path)-1]:
                self.agents_list.remove(agent)

#------------------------------------------------------------------------------# 

    def calculate_precision(self):
        count = 0

        for agent in self.agents_list:
            count += self.get_precision(agent)

        total = len(self.agents_list)

        if total > 0:
            return count/total
        else: 
            return 0
 
#------------------------------------------------------------------------------#  

    def calculate_recall(self):
        count = 0

        for agent in self.agents_list:
            count += self.get_recall(agent)

        total = len(self.agents_list)

        if total > 0:
            return count/total
        else: 
            return 0
 
#------------------------------------------------------------------------------#   

    def global_data(self, step):
        encounters = sum(agent.encounters for agent in self.agents_list)
        exchanges = sum(agent.exchanges for agent in self.agents_list)
        times = sum(agent.exec_time for agent in self.agents_list)


        self.steps.append(step)
        self.num_agents.append(len(self.agents_list))
        self.num_encounters.append(encounters)
        self.num_exchanges.append(exchanges)
        self.exec_times.append(times)

        self.precision.append(self.calculate_precision())
        self.recall.append(self.calculate_recall())

#------------------------------------------------------------------------------#            

    def next_step(self, step, similarity):
        self.generate_arrivals(step)

        for agent in self.agents_list:
                agent.move()

                if similarity == 'no_similarity':
                    agent.no_similarity(self.agents_list)

                if similarity == 'ed_similarity':
                    agent.ed_similarity(self.agents_list)

                if similarity == 'ds_similarity':
                    agent.ds_similarity(self.agents_list)


        self.global_data(step)
        self.generate_departures()

#------------------------------------------------------------------------------#
    
    def reset(self):
        self.steps = []
        self.num_agents = []
        self.num_departures = []
        self.precision = []
        self.recall = []
        self.agents_list = []
        self.n_arrivals = 0
        # No Similarity
        self.num_encounters = []
        self.num_exchanges = []
        self.exec_times = []

#------------------------------------------------------------------------------#

    def run(self, rnd, similarity):
        for step in xrange(self.duration):
            sys.stdout.write("\rExperiment: %s Round: %d Running: %d steps of %d" % (similarity, rnd, step, (self.duration-1)))
            sys.stdout.flush()
            self.next_step(step, similarity)
        print "\n" 

#==============================================================================#
