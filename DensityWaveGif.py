import numpy as np
from numpy import pi,cos,sin
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from mpl_toolkits.mplot3d import Axes3D
# from PIL import Image
'''
All the equations needed
    - v_phi is angular velocity
    - R is radius
omega = v_phi/R 
kappa = np.sqrt(R(d omega^2/d R)+4omega^2)
    d/dR(omega^2) = (-2*v_phi^2)/R^3
nu = (\partial^2 Phi)/(\partial z^2)
omega_d = omega - 0.5*kappa
phi = (omega_d+omega_0)*(T/978)+phi_D0
phi_D0 is an arbitrary offset (moves phi_d up and down)
'''

phi_d0 = 0
maxT = 978
T = np.linspace(0,maxT,maxT)
no_bodies = 10
maxR=16.2
R = np.linspace(1,maxR,no_bodies)
v_phi = 100/R 

omega_list = []
omega_d_plus_list = []
omega_d_minus_list = []
'''
We are creating a predetermined number of bodies, calculating the omega, omega_d, kappa, and nu.
Here we assume m=2.
'''

for i in range(no_bodies):
    omega = v_phi[i]/R[i]
    omega_list.append(omega)
    dOdR = np.gradient(omega**2/R[i]) 

    kappa1 = (-2*v_phi[i]**2)/R[i]**2  
    kappa = np.sqrt(kappa1+4*omega**2)

    omega_d_plus = omega+0.5*kappa
    omega_d_minus = omega-0.5*kappa
    omega_d_plus_list.append(omega_d_plus)
    omega_d_minus_list.append(omega_d_minus)

phi_d_plus_list = []
phi_d_minus_list =[]
omega_time_list=[]
omega_0 = 1.3

'''
We iterate over each body, for each time-step to determine the evolution of phi_b and phi_d with respect to radius and time.
UPDATE: the for loop was using omega_list, instead of omega_0.
'''

for t in range(maxT):
    phi_d_plus=[]
    phi_d_minus=[]
    omega_time=[]
    for i in range(no_bodies):
        time_step = T[t]/978 + phi_d0
        phi_d_plus.append((omega_d_plus_list[i]+omega_0)*time_step)
        phi_d_minus.append((omega_d_minus_list[i]+omega_0)*time_step)
        omega_time.append(omega_list[i]*time_step)
    phi_d_plus_list.append(phi_d_plus)
    phi_d_minus_list.append(phi_d_minus)
    omega_time_list.append(omega_time)

'''
Here we animate the density wave through the Milky Way, with a radius of 16.2 kpc
'''
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(1,1,1)
# fig1.set_dpi(100)
fig1,ax1 = plt.subplots(1,1)


def x(r,theta):
    return r*cos(theta)
def y(r,theta):
    return r*sin(theta)

x_d_t_plus = []
y_d_t_plus = []
x_d_t_minus = []
y_d_t_minus = []
for i in range(maxT):
    x_d_plus = []
    y_d_plus = []
    x_d_minus = []
    y_d_minus = []
    for k in range(no_bodies):
        x_d_plus.append(x(R[k],phi_d_plus_list[i][k]))
        y_d_plus.append(y(R[k],phi_d_plus_list[i][k]))
        x_d_minus.append(x(R[k],phi_d_minus_list[i][k]))
        y_d_minus.append(y(R[k],phi_d_minus_list[i][k]))
    x_d_t_plus.append(x_d_plus)
    y_d_t_plus.append(y_d_plus)
    x_d_t_minus.append(x_d_minus)
    y_d_t_minus.append(y_d_minus)

t = 0
def animate(i):
    global t
    t+=1
    ax1.clear()
    # z = np.zeros((R,1))
    ax1.plot(x_d_t_plus[t],y_d_t_plus[t],color = 'blue',label = r'$\Omega + \frac{\kappa}{2}$')
    ax1.plot(x_d_t_minus[t],y_d_t_minus[t],color = 'red',label = r'$\Omega - \frac{\kappa}{2}$')
    ax1.legend()
    ax1.set_xlim(-maxR,maxR)
    ax1.set_ylim(-maxR,maxR)
    fig1.suptitle(f't = {t}')
anim = animation.FuncAnimation(fig1,animate,frames = maxT,interval = 20)
# plt.show()
writer = PillowWriter(fps=20, codec='libx264', bitrate=2) 
anim.save("C:/Users/oasht/Documents/Uni/honours/PROJECT/GIFS/densitywave.gif",writer = writer)     