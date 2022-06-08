import unittest
import simulation
import creature
import os
import population

class TestSimulation(unittest.TestCase):

  def testSimulationExists(self):
    sim = simulation.Simulation()
    self.assertIsNotNone(sim)

  def testSimulationId(self):
    sim = simulation.Simulation()
    self.assertIsNotNone(sim.physicsClientId)

  def testRun(self):
    sim = simulation.Simulation()
    self.assertIsNotNone(sim.run_creature)

  def testRunXML(self):
    sim = simulation.Simulation()
    cr = creature.Creature(gene_count=3)
    sim.run_creature(cr)
    
    self.assertTrue(os.path.exists('temp.urdf'))

  def testPosition(self):
    sim = simulation.Simulation()
    cr = creature.Creature(gene_count=3)
    sim.run_creature(cr)
    
    self.assertNotEqual(cr.start_position, cr.last_position)
  
  def testDistance(self):
    sim = simulation.Simulation()
    cr = creature.Creature(gene_count=3)
    sim.run_creature(cr)
    dist = cr.get_distance_travelled()
    
    print("distance travelled: ", dist)
    self.assertGreater(dist, 0)

  def testPopulation(self):
    pop = population.Population(pop_size=2, gene_count=3)
    sim = simulation.Simulation()

    for cr in pop.creatures:
      sim.run_creature(cr)

    distances = [cr.get_distance_travelled() for cr in pop.creatures]
    print(distances)
    
    self.assertIsNotNone(distances)

  # def testProc(self):
  #   pop = population.Population(pop_size=20, gene_count=3)
  #   tsim = simulation.ThreadedSimulation(pool_size=8)
  #   tsim.eval_population(pop, 2400)
  #   dists = [cr.get_distance_travelled() for cr in pop.creatures]
  #   print(dists)
  #   self.assertIsNotNone(dists)

  def testProcNoThread(self):
    pop = population.Population(pop_size=20, gene_count=3)
    sim = simulation.Simulation()
    sim.eval_population(pop, 2400)
    dists = [cr.get_distance_travelled() for cr in pop.creatures]
    print(dists)
    self.assertIsNotNone(dists)


unittest.main()