import numpy as np
from numpy import pi,cos,sin
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from mpl_toolkits.mplot3d import Axes3D

#plotting stuff
fig = plt.figure()
fig.set_dpi(100)
# ax = Axes3D(fig)
ax1 = fig.add_subplot(1,1,1)
# ax2 = fig.add_subplot(2,1,1)

'''
All the equations needed
    - v_phi is angular velocity
    - R is radius
omega = v_phi/R 
kappa = np.sqrt(R(d omega^2/d R)+4omega^2)
        d/dR(omega^2) = (-2*v_phi^2)/R^3
omega_d = omega - 0.5*kappa
phi = (omega_d+omega_0)*(T/978)+phi_D0
phi_D0 is an arbitrary offset (moves phi_d up and down)
'''
phi_d0 = 0
no_time_steps = 1000
T = np.linspace(0,1000,no_time_steps)
no_bodies = 1000
maxR=10
R = np.linspace(1,maxR,no_bodies)
v_phi = 100/R 

omega_list = []
omega_d_list = []

for i in range(no_bodies):
    omega = v_phi[i]/R[i]
    omega_list.append(omega)
    dOdR = np.gradient(omega**2/R[i]) 

    kappa1 = (-2*v_phi[i]**2)/R[i]**2  
    kappa = np.sqrt(kappa1+4*omega**2)

    omega_d = omega-0.5*kappa
    omega_d_list.append(omega_d)

phi_fast_list = []
phi_slow_list=[]
for t in range(len(T)):
    phi_fast=[]
    phi_slow = []
    for i in range(no_bodies):
        phi_fast.append((omega_d_list[i]+omega_list[i])*T[t]/978+phi_d0)
        phi_slow.append((omega_d_list[i]/2+omega_list[i])*T[t]/978+phi_d0)
    phi_fast_list.append(phi_fast)
    phi_slow_list.append(phi_slow)

polar2z = lambda r,θ: r * np.exp( 1j * θ )
z2polar = lambda z: ( np.abs(z), np.angle(z) )

theta = np.linspace(0,2*pi,1000)
r,th = np.meshgrid(R,theta)

# z = polar2z(R,theta)
# plt.imshow(np.real(z),np.imag(z),phi_fast_list[1])
# plt.show()
# for i in range(len(theta)):

# print(phi_list)

t = 0
def animate(i):
    global t
    ax1.clear()
    ax1.plot(R,phi_slow_list[t],'.b-',label=r'Bending waves $\left(\frac{\Omega_d}{2}+\Omega\right)t$')
    ax1.plot(R,phi_fast_list[t],'.r-',label = r'Density waves $\left(\Omega_d+\Omega\right)t$')
    ax1.legend()  
    plt.grid(True)
    x = 't='
    y = r'for $\phi_d=0$ '
    ax1.set_title(f'{x}{t}')
    ax1.set_xlabel('Radius')
    ax1.set_ylabel(r'$\phi_d(R,t)$')
    ax1.set_ylim(0,150)
    # ax1.set_xlim(-maxR,maxR)
    t += 1
anim = animation.FuncAnimation(fig,animate,frames=360,interval=20)
# print(len(phi_fast_list[0]))
# plt.subplot(projection="polar")
# plt.pcolormesh(theta,R,phi_fast_list[0])
# plt.show()
writer = PillowWriter(fps=20, codec='libx264', bitrate=2)  
anim.save("C:/Users/oasht/Dropbox/My PC (DESKTOP-TKRDL9R)/Documents/Uni/Honours/Project/GIFS/PHI_Equations.gif",writer = writer)



