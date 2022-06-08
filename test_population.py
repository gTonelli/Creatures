import unittest
import population

class TestPop(unittest.TestCase):
  def testPopExists(self):
    pop = population.Population(pop_size=10, gene_count=4)
    self.assertIsNotNone(pop)

  def testPopHasIndividuals(self):
    pop = population.Population(pop_size=10, gene_count=4)
    self.assertEqual(len(pop.creatures), 10)

  def testFitnessMap(self):
    fitnesses = [2.5, 1.2, 3.4]
    output = [2.5, 3.7, 7.1]
    fitness_map = population.Population.get_fitness_map(fitnesses)
    self.assertEqual(fitness_map, output)

  def testSelectParent(self):
    fitnesses = [2.5, 1.2, 3.4]
    fitness_map = population.Population.get_fitness_map(fitnesses)
    pid = population.Population.select_parent_from_fitness_map(fitness_map)
    self.assertLess(pid, 3)

  def testSelectParent2(self):
    fitnesses = [0, 0, 1]
    fitness_map = population.Population.get_fitness_map(fitnesses)
    pid = population.Population.select_parent_from_fitness_map(fitness_map)
    self.assertEqual(pid, 2)


unittest.main()