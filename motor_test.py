# Not a unittest file, but rather a way to test the creation of a creature is working properly.

from time import time
import pybullet as p
import creature
import pybullet_data as pd
import time

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0, 0, -10)

c = creature.Creature(gene_count=5)

with open('motor_test.urdf', 'w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())

cid = p.loadURDF('motor_test.urdf')

p.setRealTimeSimulation(1)

while True:
    for jid in range(p.getNumJoints(cid)):
        m = c.get_motors()[jid]
        p.setJointMotorControl2(
            cid, jid, controlMode=p.VELOCITY_CONTROL, targetVelocity=m.get_output(), force=5)

    time.sleep(0.1)
