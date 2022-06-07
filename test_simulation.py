import unittest
import simulation
import creature
import os

class TestSimulation(unittest.TestCase):

  def testSimulationExists(self):
    sim = simulation.Simulation()
    self.assertIsNotNone(sim)

  def testSimulationId(self):
    sim = simulation.Simulation()
    self.assertIsNotNone(sim.physicsClientId)

  def testRun(self):
    sim = simulation.Simulation()
    # cr = creature.Creature(gene_count=3)
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
  

unittest.main()