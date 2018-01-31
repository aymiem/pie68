#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:45:59 2018

@author: arthur
"""
import timeit as tt
import pandas as pd
import numpy as np
from initialisation  import initialisation
from classement_population import rankings, choix_indiv_rg


def programme_gen(max_iter, max_time, indic_ref_1, indic_ref_2):
    print("Lancement du programme génétique")
    start = tt.default_timer()
    elapsed = 0    
    initialisation()

    for i in range(max_iter):
        while(elapsed <= max_time):
           batch = select_batch(i+1)
           
        elapsed = start - tt.default_timer()

def select_batch(gen):
    # returns 
     ranked = rankings(i+1)
     sol1 = choix_indiv_rg(ranked, i+1, indic_ref_1, 1)
     sol2 = choix_indiv_rg(ranked, i+1, indic_ref_2, 1)
     batch = np.array(range(10))
     batch = np.delete(batch, sol1)
     batch = np.delete(batch, sol2)
     batch = np.random.choice(batch, size = 3)
     
     batch = np.append(batch, [sol1,sol2])
     batch = np.add(batch, 10)
     
     return list(batch)