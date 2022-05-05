import pybullet as p
import pybullet_data as pd

print(pd.getDataPath())
p.connect(p.GUI)

plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
rob1 = p.loadURDF(pd.getDataPath() + "/cartpole.urdf")

p.setGravity(0, 0, -10)
p.setRealTimeSimulation(1)
