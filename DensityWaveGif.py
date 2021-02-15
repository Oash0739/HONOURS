import numpy as np
from numpy import pi,cos,sin
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from mpl_toolkits.mplot3d import Axes3D
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
maxT = 100
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
Applying the bending wave equations:
nu =(d^2/dz^2)Phi= 7.25 km/s (as per McMillan 2016)
Omega_b = Omega +/- nu/m
z_b = z_0* cos(2[phi-Omega_b*T])*cos(nu*T)
'''
nu = 7.25
omega_list = []
omega_b_plus_list = []
omega_b_minus_list = []

for i in range(no_bodies):
    omega = v_phi[i]/R[i]
    omega_b_plus = omega+(0.5*nu)
    omega_b_minus = omega-0.5*nu
    omega_b_plus_list.append(omega_b_plus)
    omega_b_minus_list.append(omega_b_minus)

z_0 = 2

z = lambda phi,t,omega_b: z_0*cos(2*(phi-omega_b*t)*cos(nu*t))

z_plus_time = []
z_minus_time = []
for t in range(maxT):
    z_plus = []
    z_minus = []
    for i in range(no_bodies):
        z_minus.append(z(phi_d_minus_list[t][i],T[t],omega_b_minus_list[i])) #errors might arise here
        z_plus.append(z(phi_d_plus_list[t][i],T[t],omega_b_plus_list[i]))
    z_plus_time.append(z_plus)
    z_minus_time.append(z_minus)



'''
Converting from polar to Cartesian
'''
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
xy_t = np.empty((1,maxT))
xy = np.zeros((len(y_d_plus),len(x_d_plus)))
print(xy.shape)
for t in range(maxT):
    for i in range(len(y_d_plus)):
        for j in range(len(x_d_plus)):
            xy[i][j] = z_plus_time[t]
    np.append(xy_t,xy,axis = 0)
'''
Here we animate the density wave through the Milky Way, with a radius of 16.2 kpc
'''


fig1=plt.figure()
ax1=fig1.add_subplot(111,projection = '3d')

# ax1 = fig1.add_subplot(1,1,1,projection = '3d')


# fig1,ax1 = plt.subplots(1,1)

# t = 0
# def animate(i):
#     global t
#     t+=1
#     ax1.clear()
#     # z = np.zeros((R,1))
#     # ax1.plot(x_d_t_plus[t],y_d_t_plus[t],color = 'blue',label = r'$\Omega + \frac{\kappa}{2}$')
#     ax1.plot(x_d_t_plus[t],y_d_t_plus[t],z_plus_time[t],label = r'$\Omega + \frac{\kappa}{2}$')
#     # ax1.plot(x_d_t_minus[t],y_d_t_minus[t],color = 'red',label = r'$\Omega - \frac{\kappa}{2}$')
#     ax1.legend()
#     ax1.set_xlim(-maxR,maxR)
#     ax1.set_ylim(-maxR,maxR)
#     ax1.set_zlim(-2,2)
#     fig1.suptitle(f't = {t}')
# anim = animation.FuncAnimation(fig1,animate,frames = maxT,interval = 20)
# plt.show()
# writer = PillowWriter(fps=20, codec='libx264', bitrate=2) 
# anim.save("C:/Users/oasht/Dropbox/My PC (DESKTOP-TKRDL9R)/Documents/Uni/Honours/Project/densitywave.gif",writer = writer)     