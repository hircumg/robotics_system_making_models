
import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

a = np.array([23,15+8, 15+9, 15+10])
a = a/5


x0 = 2 # Initial time
xf = 5 # Final time
N = int(2E3) # Numbers of points in time span
gpa = np.linspace(x0, xf, N) # Create time span

bmin = 3000
bmax = 20000
y = bmin + (bmax-bmin) * (((gpa-2)/3)**2.5)
b = bmin + (bmax-bmin) * (((a-2)/3)**2.5)
b = np.round(b,0)
print(f"{a}\n{b}")

plt.plot(gpa,y, 'r', linewidth=2.0)
plt.grid(color='black', linestyle='--', linewidth=1.0, alpha = 0.7)
plt.grid(True)
plt.xlim([x0, xf])
plt.show()