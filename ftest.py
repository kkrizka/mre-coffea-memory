import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import matplotlib.pyplot as plt

import tracemalloc
tracemalloc.start()

memory=[]
snapshot1=None
for fname in ['nano_dy.root']*100:
    current=tracemalloc.get_traced_memory()[0]
    memory.append(current)

    events = NanoEventsFactory.from_root(fname, schemaclass=NanoAODSchema).events()

    snapshot2 = tracemalloc.take_snapshot()
    if snapshot1 is not None:
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        print("--- [ Top 5 ] --- (total: {})".format(current))
        for stat in top_stats[:5]:
            print(stat)
    snapshot1=snapshot2

plt.plot(memory)
plt.ylabel('memory usage [bytes]')
plt.tight_layout()
plt.savefig('ftest.png')
