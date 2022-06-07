import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -10)

p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)

for i in range (10000):
  p.stepSimulation
  time.sleep(1./240.)
  print(i)

p.disconnect()