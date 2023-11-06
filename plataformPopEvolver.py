from defs import *
from math import floor
from neuralNet import NeuralNet
from plataform import Plataform

class Evolver():
  def __init__(self, population, gameDisplay):
    self.population = population 
    self.gameDisplay = gameDisplay

  def evolve_population(self):
    self._order_population_by_points()

    best_ind = self._get_best_individuals()
    worst_ind = self._get_worst_individuals()
    worst_ind = self._mutate_worst_ind(worst_ind)
    parents = best_ind + worst_ind    
    
    childs = self._breed(parents)

    self.population = parents + childs

    return self.population

  def _order_population_by_points(self):
    self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)


  def _get_best_individuals(self):
    last_best_ind = floor(GENERATION_SIZE * BEST_IND_SURVIVOR_RATE)
    return self.population[:last_best_ind]

  def _get_worst_individuals(self):
    last_worst_ind = floor(GENERATION_SIZE * WORST_IND_SURVIVOR_RATE)
    return self.population[-last_worst_ind:]

  def _mutate_worst_ind(self, worst_ind):
    for ind in worst_ind:
      ind.brain.mutate()

    return worst_ind

  def _breed(self, parents):
    childs = []
    total_of_childs = GENERATION_SIZE - len(parents)

    for i in range(total_of_childs):
      childs.append(
        Plataform(self.gameDisplay, NeuralNet.breed(parents)))

    return childs