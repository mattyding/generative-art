"""
File: randomwalk.py
-------------------
Author: Matthew Ding
Date: 08/06/2022

This file contains code for generating animations of random 2D walks.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def random_unit_vector():
    angle = np.random.random() * 2 * np.pi
    return np.cos(angle), np.sin(angle)

def random_walk(num_steps, max_step):
    x, y = np.random.random(2) * 2 - 1  # random point between -1 and 1
    steps = [(x, y)]
    for _ in range(num_steps):
        step_size = np.random.random() * max_step
        x += random_unit_vector()[0] * step_size
        y += random_unit_vector()[1] * step_size
        steps.append((x,y))
    return np.array((steps))

def update_lines(num_steps, walks, lines):
    for walk, line in zip(walks, lines):
        line.set_data(walk[:num_steps, 0], walk[:num_steps, 1])
    return lines

# https://stackoverflow.com/questions/14720331/how-to-generate-random-colors-in-matplotlib
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def random_walk_animation(num_steps, walks, cmap, seed):
    fig, ax = plt.subplots()
    lines = [ax.plot(walk[0], walk[1], color=cmap(i))[0] for i, walk in enumerate(walks)]
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.axis('off')
    anim = animation.FuncAnimation(fig, update_lines, fargs=(walks, lines),
                                   frames=num_steps, interval=100)
    #plt.show()
    plt.savefig(f"./figures/randomwalk/walk-{seed}.png")
    writergif = animation.PillowWriter(fps=30) 
    anim.save(f"./figures/randomwalk/walk-{seed}.gif" , writer=writergif)
    return fig, anim


def random_walk_stats_animation(num_steps, walks, cmap, seed):
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

    def update_graph(num_steps, walks, lines):
        for walk, line in zip(walks, lines):
            line.set_data(walk[:num_steps, 0], walk[:num_steps, 1])
        
        expectation_line.set_data(expectations_x[:num_steps], expectations_y[:num_steps])
        if num_steps > 1:
            # 0.1 buffer from edges
            expectation_plot.set_xlim(min(expectations_x[:num_steps])-0.1, max(expectations_x[:num_steps])+0.1)
            expectation_plot.set_ylim(min(expectations_y[:num_steps])-0.1, max(expectations_y[:num_steps])+0.1)
        variance_plot.clear()
        variance_plot.plot(variances[:num_steps], color='black')
        variance_plot.title.set_text('Variance')
        variance_plot.set_xlabel('Step')
        return lines

    anim = animation.FuncAnimation(fig, update_graph, fargs=(walks, lines),
                                   frames=num_steps, interval=100)
    #plt.show()
    writergif = animation.PillowWriter(fps=30) 
    anim.save(f"./figures/randomwalk/stats-{seed}.gif" , writer=writergif)
    return anim


def random_walk_art(num_steps=400, max_steps=0.15, num_walks=50):
    seed =  np.random.randint(0, 1000000)
    np.random.seed(seed)
    walks = [random_walk(num_steps, max_steps) for _ in range(num_walks)]
    cmap = get_cmap(num_walks)
    random_walk_animation(num_steps, walks, cmap, seed)
    random_walk_stats_animation(num_steps, walks, cmap, seed)


def main():
    for _ in range(10):
        num_steps = np.random.randint(200, 500)
        max_steps = np.random.uniform(0.01, 0.3)
        num_walks = np.random.randint(20, 100)
        random_walk_art(num_steps, max_steps, num_walks)


if __name__ == '__main__':
    main()
