import unittest
import population as poplib
import simulation as simlib
import creature as crlib
import genome as genlib
import numpy as np

class TestGA(unittest.TestCase):

  def testGA(self):
    population = poplib.Population(pop_size=10, gene_count=3)
    simulation = simlib.ThreadedSimulation(pool_size=1)
      
    for generation in range(10):  
      
      simulation.eval_population(population, 2400)
      fitnesses = [cr.get_distance_travelled() for cr in population.creatures]
      fitness_map = poplib.Population.get_fitness_map(fitnesses)

      print(generation, np.max(fitnesses), np.mean(fitnesses))

      fmax = np.max(fitnesses)

      for cr in population.creatures:
        if cr.get_distance_travelled() == fmax:
          elite = cr
          break

      new_gen = []

      for cid in range(len(population.creatures)):
        p1_index = poplib.Population.select_parent_from_fitness_map(fitness_map)
        p2_index = poplib.Population.select_parent_from_fitness_map(fitness_map)
        dna = genlib.Genome.crossover(population.creatures[p1_index].dna, population.creatures[p2_index].dna)
        dna = genlib.Genome.point_mutate(dna, 0.1, 0.25)
        dna = genlib.Genome.grow_mutate(dna, 0.25)
        dna = genlib.Genome.shrink_mutate(dna, 0.25)

        cr = crlib.Creature(1)
        cr.set_dna(dna)
        new_gen.append(cr)

      new_gen[0] = elite
      csv_filepath = "elites/" + str(generation) + "_elite.csv"
      genlib.Genome.dna_to_csv(elite.dna, csv_filepath)
      population.creatures = new_gen

unittest.main()