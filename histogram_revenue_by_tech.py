
import data
import matplotlib.pyplot as plt
import numpy as np

#
labels = data.quarters()

def _revenue_of_tech(tech): 
    return np.array(list(data.revenue_of_technology(tech).values()))/1000  # M NTD to B NTD

revenue_5nm = _revenue_of_tech('5nm')
revenue_7nm = _revenue_of_tech('7nm')
revenue_10nm = _revenue_of_tech('10nm')
revenue_16nm = _revenue_of_tech('16nm')

#
fig, ax = plt.subplots()

ax.bar(labels, revenue_5nm, label='revenue_5nm')
ax.bar(labels, revenue_7nm, label='revenue_7nm', bottom=revenue_5nm)
ax.bar(labels, revenue_10nm, label='revenue_10nm',bottom=revenue_5nm+revenue_7nm)
ax.bar(labels, revenue_16nm, label='revenue_16nm',bottom=revenue_5nm+revenue_7nm+revenue_10nm)

ax.set_ylabel('Billion NTD')
ax.set_title('Revenue by technology')
ax.legend()

fig.autofmt_xdate(rotation=45)
plt.grid(True)
plt.show()
