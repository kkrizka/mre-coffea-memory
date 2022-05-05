import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

import tracemalloc
tracemalloc.start()

snapshot1=None
for fname in ['nano_dy.root']*100:
    current=tracemalloc.get_traced_memory()[0]

    events = NanoEventsFactory.from_root(fname, schemaclass=NanoAODSchema).events()

    snapshot2 = tracemalloc.take_snapshot()
    if snapshot1 is not None:
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        print("--- [ Top 5 ] --- (total: {})".format(current))
        for stat in top_stats[:5]:
            print(stat)
    snapshot1=snapshot2
