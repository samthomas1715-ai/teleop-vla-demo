import numpy as np
from func import Dynamixelax

def tfm(t, alp, d, a):
    st = np.sin(t)
    ct = np.cos(t)
    sa = np.sin(a)
    ca = np.cos(a)

    return np.array([[ct, -st, 0, a],
                    [st*ca, ct*ca, -sa, -d*sa],
                    [st*sa, ct*sa, ca, d*ca],
                    [0, 0, 0, 1]])

t0 = np.deg2rad(float(input("base rotation")))
d1 = float(input("enter base to shoulder height"))
t1 = np.deg2rad(float(input("shoulder rotation")))
a1 = input("upper arm link length")
t2 = np.deg2rad(float(input("forearm rotation")))
a2 = float(input("forearm link length"))
t3 = np.deg2rad(float(input("wrist pitch")))
a3 = float(input("wrist1 length"))
t4 = np.deg2rad(float(input("yaw rotation")))
d5 = float(input("wrist2 length"))
t5 = np.deg2rad(float(input("roll rotation")))

T001 = tfm(t0, 0, d1, 0)
T011 = tfm(t1, -np.pi/2, 0, 0)
T12 = tfm(t2, 0, 0, a1)
T23 = tfm(t3, 0, 0, a2)
T331 = tfm(t3, 0, 0, a3)
T314 = tfm(t4, np.pi/2, 0, 0)
T441 = tfm(t4+(np.pi/2), 0, 0, 0)
T4142 = tfm(t4, np.pi/2, 0, 0)
T425 = tfm(t5, 0, d5, 0)

T = T001@T011@T12@T23@T331@T314@T441@T4142@T425


base = Dynamixelax(1)
shldr = Dynamixelax(2)
elb = Dynamixelax(3)
ptch = Dynamixelax(4)
yaw = Dynamixelax(5)
roll = Dynamixelax(6)


th1=base.degrees_to_position(t0)
base.moveto_pos(th1)

th2 = shldr.degrees_to_position(t1)
shldr.moveto_pos(t1)

th3 = shldr.degrees_to_position(t2)
shldr.moveto_pos(t2)

th4 = shldr.degrees_to_position(t3)
shldr.moveto_pos(t3)

th5 = shldr.degrees_to_position(t4)
shldr.moveto_pos(t4)

th6 = shldr.degrees_to_position(t5)
shldr.moveto_pos(t5)

print("x=", T[0,3])
print("y=", T[1, 3])
print("z=", T[2,3])











