from threading import Thread
import pybullet as p
from multiprocessing import Pool

class Simulation():
  def __init__(self, sim_id=0):
    self.physicsClientId = p.connect(p.DIRECT)
    self.sim_id = sim_id

  def run_creature(self, cr, iterations=2400):
    pid = self.physicsClientId
    p.resetSimulation(physicsClientId=pid)
    p.setGravity(0, 0, -10, physicsClientId=pid)
    p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId=pid)

    plane_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=pid)
    floor = p.createMultiBody(plane_shape, plane_shape, physicsClientId=pid)

    xml_file = 'temp' + str(self.sim_id) + '.urdf'
    xml_str = cr.to_xml()

    with open(xml_file, 'w') as f:
      f.write(xml_str)

    cid = p.loadURDF(xml_file, physicsClientId=pid)
    p.resetBasePositionAndOrientation(cid, [0, 0, 3], [0, 0, 0, 1], physicsClientId=pid)

    for step in range(iterations):
      p.stepSimulation(physicsClientId=pid)
      if step % 24 == 0:
        self.update_motors(cid, cr)

      position, orientation = p.getBasePositionAndOrientation(cid, physicsClientId=pid)
      cr.update_position(position)

  def update_motors(self, cid, cr):
    """
    cid is the id in the physics engine
    cr is a creature object
    jid is the id of the joint from the creature object
    """
    for jid in range(p.getNumJoints(cid, physicsClientId=self.physicsClientId)):
        m = cr.get_motors()[jid]

        p.setJointMotorControl2(
          cid, jid, controlMode=p.VELOCITY_CONTROL, 
          targetVelocity=m.get_output(), force=5, 
          physicsClientId=self.physicsClientId)

class ThreadedSimulation():
  def __init__(self, pool_size):
    self.sims = [Simulation(i) for i in range(pool_size)]

  @staticmethod
  def static_run_creature(sim, cr, iterations):
    sim.run_creature(cr, iterations)
    return cr

  def eval_population(self, pop, iterations):
    for cr in pop.creatures:
      sim.run_creature(cr, 2400)

  # def eval_population(self, pop, iterations):
  #   """
  #   pop is a Population object
  #   iterations are frames in pybullet to run for at 240fps
  #   does not work on windows, m1 macs, some intel macs yet
  #   """
  #   pool_args = []
  #   start_index = 0
  #   pool_size = len(self.sims)

  #   while start_index < len(pop.creatures):
  #     this_pool_args = []
  #     for i in range(start_index, start_index + pool_size):
  #       if i == len(pop.creatures): # the end
  #         break
  #       # work out the simulation index
  #       simulation_index = i % len(self.sims)
  #       this_pool_args.append([
  #           self.sims[simulation_index],
  #           pop.creatures[i],
  #           iterations]
  #         )
  #       pool_args.append(this_pool_args)
  #       start_index = start_index + pool_size

  #   new_creatures = []
  #   for pool_argset in pool_args:
  #     with Pool(pool_size) as p:
  #       # it works on a copy of the creatures, so receive them
  #       creatures = p.starmap(ThreadedSimulation.static_run_creature, pool_argset)
  #       # and now put those creatures back into the main
  #       # self.creatures array
  #       new_creatures.extend(creatures)
  #     pop.creatures = new_creatures


