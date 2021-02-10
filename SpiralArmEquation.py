import numpy as np
from numpy import pi,cos,sin
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from mpl_toolkits.mplot3d import Axes3D

#plotting stuff
fig, ax = plt.subplots(2, 1, constrained_layout=True,figsize=(15,15))
fig.set_dpi(200)
# ax = Axes3D(fig)


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
T = np.linspace(0,1000,no_time_steps)
no_bodies = 1000
maxR=20
R = np.linspace(1,maxR,no_bodies)
v_phi = 100/R 

omega_list = []
omega_d_list = []
omega_b_list = []

for i in range(no_bodies):
    omega = v_phi[i]/R[i]
    omega_list.append(omega)
    dOdR = np.gradient(omega**2/R[i]) 

    kappa1 = (-2*v_phi[i]**2)/R[i]**2  
    kappa = np.sqrt(kappa1+4*omega**2)

    # nu = 

    omega_d = omega-0.5*kappa
    omega_d_list.append(omega_d)

phi_d_plus_list = []
phi_d_minus_list =[]
phi_b_plus_list = []
phi_b_minus_list=[]
omega_time_list=[]
for t in range(len(T)):
    phi_d_plus=[]
    phi_d_minus=[]
    phi_b_plus=[]
    phi_b_minus = []
    omega_time=[]
    for i in range(no_bodies):
        phi_d_plus.append((omega_d_list[i]+omega_list[i])*T[t]/978+phi_d0)
        phi_d_minus.append((omega_d_list[i]-omega_list[i])*T[t]/978+phi_d0)
        phi_b_plus.append((omega_d_list[i]/2+omega_list[i])*T[t]/978+phi_d0)
        phi_b_minus.append((omega_d_list[i]/2-omega_list[i])*T[t]/978+phi_d0)
        omega_time.append(omega_list[i]*T[t]/978+phi_d0)
    phi_d_plus_list.append(phi_d_plus)
    phi_d_minus_list.append(phi_d_minus)
    phi_b_plus_list.append(phi_b_plus)
    phi_b_minus_list.append(phi_b_minus)
    omega_time_list.append(omega_time)


t = 0
def animate(i):
    global t
    ax[0].clear()
    ax[1].clear()
    ax[0].plot(R,phi_b_plus_list[t],label=r' $\left(\frac{\Omega_d}{2}+\Omega\right)t$',linewidth = 0.1,linestyle = 'dashdot',color = 'blue')
    ax[0].plot(R,omega_time_list[t],'k',label = r'$\Omega',linewidth=0.1)
    ax[0].plot(R,phi_b_minus_list[t],label=r' $\left(\frac{\Omega_d}{2}-\Omega\right)t$',linewidth=0.1,linestyle = 'dashed',color = 'red')
    ax[1].plot(R,phi_d_plus_list[t],label=r'$\left(\Omega_d+\Omega\right)t$',linewidth=0.10,linestyle = 'dashdot',color = 'blue')
    ax[1].plot(R,omega_time_list[t],'k',label = r'$\Omega',linewidth=0.1)
    ax[1].plot(R,phi_d_minus_list[t],label = r'$\left(\Omega_d-\Omega\right)t$',linewidth=0.1,linestyle = 'dashed',color = 'red')
    ax[0].legend()  
    ax[1].legend()
    x='t='
    fig.suptitle(f'{x}{t}')
    ax[0].set_title('Bending waves')
    ax[1].set_title('Density waves')
    ax[0].set_xlabel('Radius')
    ax[0].set_ylabel(r'$\phi_d(R,t)$')
    ax[0].set_ylim(0,max(phi_d_plus_list[-1]))
    ax[1].set_ylim(0,max(phi_d_plus_list[-1]))
    # ax1.set_xlim(-maxR,maxR)
    t += 1
anim = animation.FuncAnimation(fig,animate,frames=360,interval=20)
plt.show()
# writer = PillowWriter(fps=20, codec='libx264', bitrate=2) 
# filelocatation = "C:/Users/oasht/Documents/Uni/honours/PROJECT/GIFS" 
# filename = "PHI_Equations.gif"
# filename = filelocatation+filename
# anim.save(filename,writer = writer)


