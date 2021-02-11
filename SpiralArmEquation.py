'''
Oliver Ashton 2021
School of Physics, The University of Sydney
Spiral Arm Equation as per Hawthorn-Bland & Garcia, 2020
We are aimming animate the density wave and bending wave propergation through a Galaxy using the equations below
'''

import numpy as np
from numpy import pi,cos,sin
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from mpl_toolkits.mplot3d import Axes3D

# Figure creation
fig, ax = plt.subplots(2, 1, constrained_layout=True)
fig.set_dpi(100)

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
no_time_steps = 1000
maxT = 978
T = np.linspace(0,maxT,no_time_steps)
no_bodies = 1000
maxR=20
R = np.linspace(1,maxR,no_bodies)
v_phi = 100/R 

omega_list = []
omega_d_plus_list = []
omega_d_minus_list = []
omega_b_plus_list = []
omega_b_minus_list = []

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

    # nu =  #maybe the same as kappa but we shall find out

    omega_d_plus = omega+0.5*kappa
    omega_d_minus = omega-0.5*kappa
    omega_d_plus_list.append(omega_d_plus)
    omega_d_minus_list.append(omega_d_minus)

    # omega_b_plus = omega+0.5*nu
    # omega_b_minus = omega+0.5*nu
    # omega_b_plus_list.append(omega_b_plus)
    # omega_b_minus_list.append(omega_b_minus)

phi_d_plus_list = []
phi_d_minus_list =[]
phi_b_plus_list = []
phi_b_minus_list=[]
omega_time_list=[]
omega6_time_list=[]
omega_0 = 1.3

'''
We iterate over each body, for each time-step to determine the evolution of phi_b and phi_d with respect to radius and time.
UPDATE: the for loop was using omega_list, instead of omega_0.
'''

for t in range(no_time_steps):
    phi_d_plus=[]
    phi_d_minus=[]
    phi_b_plus=[]
    phi_b_minus = []
    omega_time=[]
    omega6_time=[]
    for i in range(no_bodies):
        time_step = T[t]/978 + phi_d0
        phi_d_plus.append((omega_d_plus_list[i]+omega_0)*time_step)
        phi_d_minus.append((omega_d_minus_list[i]+omega_0)*time_step)
        phi_b_plus.append((omega_d_plus_list[i]/2+omega_0)*time_step) #change to omega_b_plus_list
        phi_b_minus.append((omega_d_minus_list[i]/2+omega_0)*time_step) #change to omega_b_minus_list
        omega_time.append(omega_list[i]*time_step)
        omega6_time.append(omega_list[i]*time_step/6)
    phi_d_plus_list.append(phi_d_plus)
    phi_d_minus_list.append(phi_d_minus)
    phi_b_plus_list.append(phi_b_plus)
    phi_b_minus_list.append(phi_b_minus)
    omega_time_list.append(omega_time)
    omega6_time_list.append(omega6_time)


t = 0
def animate(i):
    global t
    ax[0].clear()
    ax[1].clear()
    linewide = 3
    ax[0].plot(R,phi_b_plus_list[t],label=r' $\Omega + \frac{\nu}{m}$',linewidth = linewide,linestyle = 'dashdot',color = 'blue')
    ax[0].plot(R,omega_time_list[t],'k',label = r'$\Omega$',linewidth=linewide)
    ax[0].plot(R,phi_b_minus_list[t],label=r' $\Omega - \frac{\nu}{m}$',linewidth=linewide,linestyle = 'dashed',color = 'red')
    ax[1].plot(R,phi_d_plus_list[t],label=r'$\Omega + \frac{\kappa}{m}$',linewidth=linewide,linestyle = 'dashdot',color = 'blue')
    ax[1].plot(R,omega_time_list[t],'k',label = r'$\Omega$',linewidth=linewide)
    ax[1].plot(R,phi_d_minus_list[t],label = r'$\Omega - \frac{\kappa}{m}$',linewidth=linewide,linestyle = 'dashed',color = 'red')
    ax[1].plot(R,omega6_time_list[t],label=r'$\frac{\Omega}{6}$',linewidth=linewide,color='black',linestyle = 'dotted')
    ax[0].legend(title = r'$\Omega_b =$ ')  
    ax[1].legend(title = r'$\Omega_d =$ ')
    b = r'$\phi_b($'
    d = r'$\phi_d($'
    comma = ','
    close = ')'
    yes = max(phi_b_plus_list[t])
    yep = max(phi_d_plus_list[t])
    equal = '='
    ax[0].annotate(f'{b}{1}{comma}{t}{close}{equal}{yes}', (1,max(phi_b_plus_list[t])))
    ax[1].annotate(f'{d}{1}{comma}{t}{close}{equal}{yep}', (1,max(phi_d_plus_list[t])))
    x='t='
    myr = 'Myr'
    fig.suptitle(f'{x}{t}{myr}')
    ax[0].set_title(r'Bending waves for $m=2$ $\Omega_b + \Omega$ ')
    ax[1].set_title(r'Density waves for $m=2$ $\Omega_d + \Omega$ ')
    ax[1].set_xlabel(r'Radius (kpc)')
    ax[0].set_ylabel(r'$\phi_d(R,t)$ (km s$^{-1}$ kpc$^{-1}$)')
    ax[1].set_ylabel(r'$\phi_b(R,t)$ (km s$^{-1}$ kpc$^{-1}$)')
    ax[0].set_ylim(0,max(phi_d_plus_list[-1]))
    ax[1].set_ylim(0,max(phi_d_plus_list[-1]))
    t += 1
anim = animation.FuncAnimation(fig,animate,frames=no_time_steps,interval=20)
# plt.show()
writer = PillowWriter(fps=20, codec='libx264', bitrate=2) 
filelocation = "C:/Users/oasht/Documents/Uni/honours/PROJECT/GIFS" #change \ to /
filename = "/PHI_Equations.gif" #make sure to add / to the beginning
filename = filelocation+filename
anim.save(filename,writer = writer)
