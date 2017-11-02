# -*- coding: utf-8 -*-

import re
import random as rd
import numpy as np
import time as time
from haversine import haversine

#------------------------------------------------------------------------------#

import Geo

#------------------------------------------------------------------------------#


global alpha
global beta 
#low: 5, 1
#high: 1, 5
#med: 2, 2 
alpha = 5
beta = 1


#==============================================================================#
#--- Class: Agent -------------------------------------------------------------#
#==============================================================================#

class Agent(object):
    def __init__(self, path = [], interests = [], documents = [], classifications = {}, finished = False):
        self.path = path
        self.pos = path[0]
        self.next_pos = 1

        self.walk_distance = 1.3 # 1.3 meters/ sec - average human speed
        self.proximity = 0.10 #10 meters
        self.finished_path = finished

        self.doc_classes = classifications
        self.interests = self.set_interests(interests)
        self.documents = self.set_documents(documents)

        #--- Statistical Data ---#
        self.encounters = 0
        self.exchanges = 0
        self.exec_time = 0

        

#------------------------------------------------------------------------------#

    def set_new_path(self, new_path):
        self.path = []

        if self.path == []:
            self.path = new_path
            return True
        else:
            return False

#------------------------------------------------------------------------------#

    # Creates a random sized list of itens from another list
    def set_interests(self, list_of_items):
        items = []

        if list_of_items:
            for i in list_of_items:
                r = rd.randint(-1, 1)
                tup = [i, r]
                items.append(tup)
        else:
            print "Warning: list of items is empty!"

        return items

#------------------------------------------------------------------------------#

    def get_docs_by_interest(self, search_interest):
        for key, documents in self.doc_classes.iteritems():
            if key == search_interest:
                return documents

#------------------------------------------------------------------------------#

    def set_documents(self, list_of_docs):
        docs_dict = {} 
        for interest in self.interests:
            if interest[1] == 1:
                aux_list = self.get_docs_by_interest(interest[0])
                docs_dict[interest[0]] = rd.sample(aux_list, rd.randint(0, 2)) # len(aux_list)/2))
        return docs_dict

#------------------------------------------------------------------------------#

# Getting distance from self to another agent on the list
    def get_distance(self, agent):
            if id(self) != id(agent):
                return haversine((self.pos[0], self.pos[1]), (agent.pos[0], agent.pos[1]))
            else:
                return float(10e9)

#------------------------------------------------------------------------------#

    def dempster_shafer(self, m1, m2):    
        k1 = m1.keys()
        k2 = m2.keys()

        product = [{} for i in range(len(m1))]

        for i in range(len(m1)):
            for j in range(len(m2)):
                key = k1[i] + k2[j]
                product[i][key] = m1[k1[i]]*m2[k2[j]]
        m3 = {}
        for i in range(len(product)):
            k3=product[i].keys()
            for j in range(len(k3)):
                matchObj = re.compile( r'a{1}')
                if len(matchObj.sub( '', k3[j], count=1)) == 1:
                    m3[matchObj.sub( '', k3[j], count=1)] = product[i][k3[j]]
                else:
                    denominator = 1.0 - product[i][k3[j]]

        k3 = m3.keys()
        for i in range(len(k3)):
            m3[k3[i]] = m3[k3[i]] / denominator

        return m3

#==============================================================================#

    # def move(self):
    #     if self.next_pos < len(self.path):
    #         angle = Geo.calculate_angle(self.pos, self.path[self.next_pos])
    #         self.pos = Geo.calculate_next_point(self.pos, self.walk_distance, angle)

    #         if haversine(self.pos, self.path[self.next_pos]) < 0.011:
    #             self.pos = self.path[self.next_pos]

    #         self.next_pos += 1
            
    #     # elif self.pos == self.path[len(agent.path)-1]:
    #     #     self.finished_path = True

    def move(self):
        if self.next_pos < len(self.path):
            while haversine(self.pos, self.path[self.next_pos]) >= 0.010:
                angle = Geo.calculate_angle(self.pos, self.path[self.next_pos])
                self.pos = Geo.calculate_next_point(self.pos, self.walk_distance, angle)

            self.pos = self.path[self.next_pos]
            # This line of code bellow MUST NOT BE ABSSENT or there will be unforeseen consequences
            self.next_pos += 1 

#------------------------------------------------------------------------------#

    def exchange(self, agent, chance = 0.5):
        exchange_chance = chance
        cont_exchange = 0

        # Verify matching interests from another agent
        for index, interest in enumerate(agent.interests):

            if self.interests[index][1] == 1 and agent.interests[index][1] == 1:

                # Find classifications of documents of self and agent
                self_docs = set(self.documents[interest[0]])
                agent_docs = set(agent.documents[interest[0]])
            
                # Get the mismatches and conduct the exchanges of documents
                docs_difference = self_docs.symmetric_difference(agent_docs)

                for doc in docs_difference:
                    if np.random.beta(alpha, beta) >= exchange_chance:

                        if doc not in self.documents[interest[0]]: 
                            self.documents[interest[0]].append(doc)
                            cont_exchange += 1

                    elif np.random.uniform(0, 1) >= exchange_chance:
                        self.documents[interest[0]].append(doc)
                        cont_exchange += 1

                    else:
                        exchange_chance -= 0.01
        return cont_exchange

#------------------------------------------------------------------------------#

    def no_similarity(self, agents_list):
        lengh_items = len(self.interests)
        aux = 0

        for agent in agents_list:
            if self.get_distance(agent) <= self.proximity:
                self.encounters += 1

                #--- Exchanges with NPS ---------------------------------------#
                start = (time.time() * 1000.0) 

                self.exchanges += self.exchange(agent)

                end = (time.time() * 1000.0)

                self.exec_time += (end - start)

#------------------------------------------------------------------------------#

    def ed_similarity(self, agents_list):
        lengh_items = len(self.interests)
        exec_time = 0

        for agent in agents_list:
            if self.get_distance(agent) <= self.proximity:
                self.encounters += 1

                #--- Calculating Euclidean Distance ---------------------------# 
                x = np.array([item[1] for item in self.interests])
                y = np.array([item[1] for item in agent.interests])
                prob = np.linalg.norm(x - y) / (2 * np.sqrt(lengh_items)) # Euclidean Distance / 2*Square Root

                # --- Exchanges with EDS ---------------------------------------#
                start = (time.time() * 1000.0)

                if np.random.beta(alpha, beta) < prob: # Chance of exchanging on encounter
                    self.exchanges += self.exchange(agent, prob)

                end = (time.time() * 1000.0) 
                self.exec_time += (end - start)

#------------------------------------------------------------------------------#
    
    def ds_similarity(self, agents_list):
        lengh_items = len(self.interests)
        exec_time = 0

        for agent in agents_list:
            if self.get_distance(agent) <= self.proximity:
                self.encounters += 1
    
                #--- Calculating Euclidean Distance ---------------------------# 
                x = np.array([item[1] for item in self.interests])
                y = np.array([item[1] for item in agent.interests])
                prob = np.linalg.norm(x - y) / (2 * np.sqrt(lengh_items)) # Euclidean Distance / 2*Square Root


                # --- Exchanges with DSS ---------------------------------------#  
                e1 = {}  # First evidence = e1(similar)
                e1["s"] = prob
                e1["a"] = 1 - prob

                e2 = {} # Second evidence = e2(not similar)
                value = np.random.beta(alpha, beta)
                e2["d"] = abs(value - prob)
                e2["a"] = 1 - value

                e3 = self.dempster_shafer(e1, e2)
                 
                start = (time.time() * 1000.0) 

                if e3['s'] > e3['d']:
                    self.exchanges += self.exchange(agent, e3['s'])

                end = (time.time() * 1000.0) 
                self.exec_time += (end - start)


#==============================================================================#