from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

import sys
if len(sys.argv)==1:
    print('usage: {0} input.root [input.root]'.format(sys.argv[0]))
    sys.exit(0)

import tracemalloc
tracemalloc.start()

snapshot1=None
for fname in sys.argv[1:]*100:
    #events = NanoEventsFactory.from_root(fname, schemaclass=NanoAODSchema).events()
    events = NanoEventsFactory.from_root(fname).events()
    current=tracemalloc.get_traced_memory()[0]

    snapshot2 = tracemalloc.take_snapshot()
    if snapshot1 is not None:
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        print("--- [ Top 5 ] --- (total: {})".format(current))
        for stat in top_stats[:5]:
            print(stat)
    snapshot1=snapshot2
