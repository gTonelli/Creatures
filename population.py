import creature
import numpy as np

class Population():
  def __init__(self, pop_size, gene_count):
    self.creatures = [creature.Creature(gene_count=gene_count) for i in range(pop_size)]

  @staticmethod
  def get_fitness_map(fitnesses):
    fitness_map = []
    total = 0
    for f in fitnesses:
      total = total + f
      fitness_map.append(total)

    return fitness_map

  @staticmethod
  def select_parent_from_fitness_map(fitness_map):
    r = np.random.rand()
    r = r * fitness_map[-1]
    for i in range(len(fitness_map)):
      if r <= fitness_map[i]:
        return i