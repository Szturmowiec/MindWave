import json
import matplotlib.pyplot as plt
import pandas as pd

with open('brain_scan.json') as f:
    data = json.load(f)


def draw_xcoords(ax):
    xcoords = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for xc in xcoords:
        ax.axvline(x=xc, c='gray', linewidth=0.75)


print(len(data))

i = 0
cycle = 0
attention = []
meditation = []
highAlpha = []
lowAlpha = []
highBeta = []
lowBeta = []
delta = []
lowGamma = []
midGamma = []
theta = []
for image in data:
    i += 1
    attention.extend(data[image]['attention'])
    meditation.extend(data[image]['meditation'])
    highAlpha.extend(data[image]['highAlpha'])
    lowAlpha.extend(data[image]['lowAlpha'])
    highBeta.extend(data[image]['highBeta'])
    lowBeta.extend(data[image]['lowBeta'])
    delta.extend(data[image]['delta'])
    lowGamma.extend(data[image]['lowGamma'])
    midGamma.extend(data[image]['midGamma'])
    theta.extend(data[image]['theta'])
    print(image)
    if image == 'Camping 9.jpg':
        print(f'Ending at {i} image')
        break

    if (i % 10) is 0:
        cycle += 1
        fig, axs = plt.subplots(3, 2)
        axs[0, 0].plot(attention, 'red', label="attention")
        axs[0, 0].plot(meditation, 'black', label="meditation")
        draw_xcoords(axs[0, 0])
        axs[0, 0].legend()
        axs[0, 1].plot(highAlpha, 'darkgreen', label="highAlpha")
        axs[0, 1].plot(lowAlpha, 'lime', label="lowAlpha")
        draw_xcoords(axs[0, 1])
        axs[0, 1].legend()
        axs[1, 0].plot(highBeta, 'purple', label="highBeta")
        axs[1, 0].plot(lowBeta, 'deeppink', label="lowBeta")
        draw_xcoords(axs[1, 0])
        axs[1, 0].legend()
        axs[1, 1].plot(lowGamma, 'darkgoldenrod', label="lowGamma")
        axs[1, 1].plot(midGamma, 'gold', label="midGamma")
        draw_xcoords(axs[1, 1])
        axs[1, 1].legend()
        axs[2, 0].plot(delta, 'navy', label="delta")
        draw_xcoords(axs[2, 0])
        axs[2, 0].legend()
        axs[2, 1].plot(theta, 'navy', label="theta")
        draw_xcoords(axs[2, 1])
        axs[2, 1].legend()
        fig.suptitle(f'Set number {cycle}', fontsize=16)
        plt.savefig(f'Set-number-{cycle}')
        plt.show()

        corr = pd.Series(attention).corr(pd.Series(meditation))
        print(corr)

        attention = []
        meditation = []
        highAlpha = []
        lowAlpha = []
        highBeta = []
        lowBeta = []
        delta = []
        lowGamma = []
        midGamma = []
        theta = []
