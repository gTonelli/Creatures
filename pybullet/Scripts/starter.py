import pybullet as p
import time

p.connect(p.GUI)

p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0, 0, -10)


def step_sequence(rob):
    mode = p.POSITION_CONTROL

    for i in range(10):
        p.setJointMotorControl2(rob, 0, controlMode=mode, targetPosition=i)
        time.sleep(0.5)


def switch_motors_on(r, s):
    mode = p.VELOCITY_CONTROL
    # r / robot, s / speed
    for jid in range(p.getNumJoints(r)):
        p.setJointMotorControl2(r, jid, controlMode=mode, targetVelocity=s)
