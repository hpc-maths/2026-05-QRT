from io import StringIO
import requests

import numpy as np
from scipy.optimize import curve_fit
from mpl_toolkits.axisartist.axislines import AxesZero
import matplotlib.pyplot as plt

path = (
    "https://raw.githubusercontent.com/karlrupp/microprocessor-trend-data/master/50yrs/"
)
files = [
    ("cores", 1, "Number of cores"),
    ("frequency", 1, "Frequency (MHz)"),
    ("specint", 1, "SpecInt performance (x$10^3$) on one thread"),
    ("transistors", 1e-3, "Number of transistors (thousands)"),
    ("watts", 1, "Power consumption (Watts)"),
]


def linear(x, a, b):
    return a * x + b


def tanh(x, a, b, c, d):
    return a * np.tanh((x - b) / c) + d


plt.style.use("dark_background")

fig, ax = plt.subplots()

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set(
    xlim=(1970, 2025),
    xticks=np.arange(1970, 2022, step=10),
    ylim=(-0.5, 9),
    yticks=np.arange(0, 9),
    yticklabels=[f"$10^{{ {i} }}$" for i in range(0, 9)],
)

for file, scale, legend in files:
    data = np.loadtxt(StringIO(requests.get(f"{path}/{file}.dat").text))
    x, y = data[:, 0], np.log10(data[:, 1])

    if file == "transistors":
        popt, pcov = curve_fit(linear, x, y)
        fit = linear(x, *popt)
    else:
        popt, pcov = curve_fit(
            tanh, x, y, bounds=([0.01, 1971, 0.01, 1e-6], [50, 2030, 50, 10])
        )
        fit = tanh(x, *popt)

    ax.plot(x, fit, label=legend)
    ax.scatter(x, y, alpha=0.5)

ax.legend(fontsize=8)
ax.grid(ydata=[], linestyle=":", alpha=0.5)
ax.set_xlabel("year")
# ax.set_ylabel('logarithmic scale')
plt.savefig("cpu_trends.svg", dpi=600, transparent=True)
# plt.show()
