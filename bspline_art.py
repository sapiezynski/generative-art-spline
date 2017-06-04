from bspline import bspline
import matplotlib.pyplot as plt
import numpy as np
import time as time
import math

def noise(x, y, line_count, noise_type='gradient'):
    if noise_type == 'gradient':
        return np.random.randn(x.shape[0],)*x*(y+1)/(x.shape[0]*2*(line_count))
    elif noise_type == 'circle':
        return np.random.randn(x.shape[0],)\
    *np.sin(x*math.pi/x.shape[0])\
    *np.cos((y-line_count/2.0)*math.pi/line_count)/2.5
    elif noise_type == 'sin2':
        return np.random.randn(x.shape[0],)\
    *np.sin(x*math.pi/x.shape[0])**2\
    *np.cos((y-line_count/2.0)*math.pi/line_count)**2/2.5
    elif noise_type == 'unknown_pleasures':
        g1 = np.random.randn(10000)*x.shape[0]/20.0+x.shape[0]*1.25/3.0
        g2 = np.random.randn(10000)*2*x.shape[0]/20.0 + x.shape[0]*1.75/3.0
        h1 = np.histogram(g1, bins=np.arange(0, x.shape[0]+1))[0]/200
        h2 = np.histogram(g2, bins=np.arange(0, x.shape[0]+1))[0]/200
        
        return (h1 + h2)*(np.random.randn(x.shape[0],)+3)/15+np.random.randn(x.shape[0],)/20



def generate(line_color='k', 
             background_color='w',
             noise_type='gradient', 
            line_count=20,
            inner_reps=100,
            outer_reps=5,
            randomize_x=True):
    
    length = 100
    spacing = 1
    
    f, ax = plt.subplots()

    x = np.arange(0, length, 1)
    for y in range(0, line_count):
        for main_rep in range(0, outer_reps):
            n = noise(x, y, line_count, noise_type=noise_type)
            for repetition in range(0, inner_reps):
                if randomize_x:
                    cv = np.stack((x+np.random.randn()*2*n, n*((np.random.randn()/2+1)))).transpose()
                else:
                    cv = np.stack((x, n*((np.random.randn()/2+1)))).transpose()
                yspline = bspline(cv, n=200, degree=10)
                plt.plot(yspline[:,0], yspline[:,1]-y*spacing, 
                         color=line_color, alpha=20.0/inner_reps, ls='-', lw=.1)

    ax.set_frame_on(False)

    ax.set_yticks([])
    ax.set_xticks([])
    f.patch.set_facecolor(background_color)
    f.set_size_inches(20, 20)

    f.savefig('%s_%d.png'%(noise_type, int(time.time())))

def generate_joy(length=50, spacing=1, line_count=70, repetitions=100,
            line_color='#fffff2', 
            background_color=(0, 0, 0),
            noise_type='unknown_pleasures'):
    
    f, ax = plt.subplots()


    x = np.arange(0, length, 1)
    for y in range(0, line_count):
        n = noise(x, y, line_count, noise_type=noise_type)
        for repetition in range(0, repetitions):
            cv = np.stack((x, n*((np.random.randn()/50+1)))).transpose()
            plt.plot(cv[:,0], cv[:,1]-y*spacing, 
                     color=line_color, alpha=.2, ls='-', lw=1, zorder=y)
            plt.fill_between(cv[:,0], -line_count*2, cv[:,1]-y*spacing, color=background_color, zorder=y)

    ax.set_frame_on(False)
    ax.set_ylim(-line_count, 3)

    ax.set_yticks([])
    ax.set_xticks([])
    f.patch.set_facecolor(background_color)
    f.set_size_inches(14, 20)

    f.savefig('%s_%d.png'%(noise_type, int(time.time())), facecolor=f.get_facecolor())