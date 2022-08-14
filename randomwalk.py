"""
File: randomwalk.py
-------------------
Author: Matthew Ding
Date: 08/06/2022

This file contains code for generating animations of random 2D walks.
"""
import os
from signal import pause
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

FRAME_SKIP = 4  # for reducing the size of the file
PAUSE_RATIO = 0.6

def random_unit_vector():
    angle = np.random.random() * 2 * np.pi
    return np.cos(angle), np.sin(angle)

def random_walk(num_steps, max_step):
    x, y = np.random.random(2) * 2 - 1  # random points between -1 and 1
    steps = [(x, y)]
    for _ in range(num_steps * FRAME_SKIP):
        step_size = np.random.random() * max_step
        ang_x, ang_y = random_unit_vector()
        x += ang_x * step_size
        y += ang_y * step_size
        steps.append((x,y))
    return np.array((steps))


def update_lines(num_steps, walks, lines, pause_threshold):
    for walk, line in zip(walks, lines):
        if num_steps < pause_threshold:
            line.set_data(walk[:num_steps*FRAME_SKIP, 0], walk[:num_steps*FRAME_SKIP, 1])
        else:  # pause animation at end
            line.set_data(walk[:pause_threshold*FRAME_SKIP, 0], walk[:pause_threshold*FRAME_SKIP, 1])
    return lines

# https://stackoverflow.com/questions/14720331/how-to-generate-random-colors-in-matplotlib
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def random_walk_animation(params, walks, cmap, seed):
    num_steps, max_step_size, num_walks = params
    pause_threshold = int(num_steps * PAUSE_RATIO)

    fig, ax = plt.subplots()
    lines = [ax.plot(walk[0], walk[1], color=cmap(i))[0] for i, walk in enumerate(walks)]
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.axis('off')
    anim = animation.FuncAnimation(fig, update_lines, fargs=(walks, lines, pause_threshold),
                                   frames=num_steps, interval=100)
    #plt.show()
    plt.savefig(f"./figures/randomwalk/{seed}-{num_steps}-{max_step_size}-{num_walks}/walk-full.png", dpi=500)
    writergif = animation.PillowWriter(fps=20) 
    anim.save(f"./figures/randomwalk/{seed}-{num_steps}-{max_step_size}-{num_walks}/walk.gif" , writer=writergif)

    fig.savefig(f"./figures/randomwalk/{seed}-{num_steps}-{max_step_size}-{num_walks}/walk-small.png", dpi=500)


def random_walk_stats_animation(params, walks, cmap, seed):
    num_steps, max_step_size, num_walks = params
    pause_threshold = int(num_steps * PAUSE_RATIO)

    fig, _ = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(10)
    plt.subplots_adjust(hspace=0.5)
    expectations = [(np.mean([walk[i][0] for walk in walks]), np.mean([walk[i][1] for walk in walks])) for i in range(len(walks[0]))]
    expectations_x = [expectation[0] for expectation in expectations]
    expectations_y = [expectation[1] for expectation in expectations]
    variances = [np.mean([(expectations[i] - walk[i]) ** 2 for walk in walks]) for i in range(len(walks[0]))]

    walk_plot = plt.subplot2grid((2, 4), (0, 0), rowspan=2, colspan=2)
    walk_plot.set_xlim(-1, 1)
    walk_plot.set_ylim(-1, 1)
    walk_plot.axis('off')
    lines = [walk_plot.plot(walk[0], walk[1], color=cmap(i))[0] for i, walk in enumerate(walks)]
    expectation_plot = plt.subplot2grid((2, 4), (0, 3), rowspan=1, colspan=2)
    expectation_plot.title.set_text('Expectation')
    expectation_plot.xaxis.grid(True, which='major')
    expectation_plot.yaxis.grid(True, which='major')
    expectation_plot.set_xlabel('x')
    expectation_plot.set_ylabel('y', rotation=0)
    expectation_line = expectation_plot.plot(expectations[0][0], expectations[0][1], color='black')[0]

    variance_plot = plt.subplot2grid((2, 4), (1, 3), rowspan=1, colspan=2)

    def update_graph(num_steps, walks, lines, pause_threshold):
        lines = update_lines(num_steps, walks, lines, pause_threshold)

        variance_plot.clear()
        variance_plot.title.set_text('Variance')
        variance_plot.set_xlabel('Step')

        if num_steps < pause_threshold:
            expectation_line.set_data(expectations_x[:num_steps*FRAME_SKIP], expectations_y[:num_steps*FRAME_SKIP])
            if num_steps > 1:
                # 0.1 buffer from edges
                expectation_plot.set_xlim(min(expectations_x[:num_steps*FRAME_SKIP])-0.1, max(expectations_x[:num_steps*FRAME_SKIP])+0.1)
                expectation_plot.set_ylim(min(expectations_y[:num_steps*FRAME_SKIP])-0.1, max(expectations_y[:num_steps*FRAME_SKIP])+0.1)
                variance_plot.plot(variances[:num_steps*FRAME_SKIP], color='black')
        else:
            expectation_line.set_data(expectations_x[:pause_threshold*FRAME_SKIP], expectations_y[:pause_threshold*FRAME_SKIP])
            if num_steps > 1:
                # 0.1 buffer from edges
                expectation_plot.set_xlim(min(expectations_x[:pause_threshold*FRAME_SKIP])-0.1, max(expectations_x[:pause_threshold*FRAME_SKIP])+0.1)
                expectation_plot.set_ylim(min(expectations_y[:pause_threshold*FRAME_SKIP])-0.1, max(expectations_y[:pause_threshold*FRAME_SKIP])+0.1)
                variance_plot.plot(variances[:pause_threshold*FRAME_SKIP], color='black')
        return lines

    anim = animation.FuncAnimation(fig, update_graph, fargs=(walks, lines, pause_threshold),
                                   frames=num_steps, interval=100)
    #plt.show()
    writergif = animation.PillowWriter(fps=20) 
    anim.save(f"./figures/randomwalk/{seed}-{num_steps}-{max_step_size}-{num_walks}/stats.gif" , writer=writergif)


def random_walk_art(num_steps=400, max_step_size=0.15, num_walks=50):
    seed = np.random.randint(0, 1000000)
    np.random.seed(seed)
    os.mkdir(f"{os.getcwd()}/figures/randomwalk/{seed}-{num_steps}-{max_step_size}-{num_walks}")
    walks = [random_walk(num_steps, max_step_size) for _ in range(num_walks)]
    cmap = get_cmap(num_walks)
    random_walk_animation((num_steps, max_step_size, num_walks), walks, cmap, seed)
    random_walk_stats_animation((num_steps, max_step_size, num_walks), walks, cmap, seed)


def main():
    num_steps = np.random.randint(100, 150)
    max_step_size = np.random.uniform(0.01, 0.3)
    num_walks = np.random.randint(20, 100)
    random_walk_art(num_steps, round(max_step_size, 2), num_walks)


if __name__ == '__main__':
    main()
