import pybullet as p
import time

pClient = p.connect(p.GUI)
x = p.loadURDF("syn_p0.urdf")
x = p.loadURDF("syn_p1.urdf")
x = p.loadURDF("syn_p2.urdf")
x = p.loadURDF("syn_p3.urdf")
x = p.loadURDF("syn_p4.urdf")
y = p.getCameraImage(512, 512)
time.sleep(10)
p.disconnect()