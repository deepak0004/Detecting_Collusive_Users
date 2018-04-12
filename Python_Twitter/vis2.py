import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

uniform_data = np.random.rand(10, 12)
print uniform_data
ax = sns.heatmap(uniform_data, linewidth=0.5)
plt.show()