Tries to reproduce a memory leak in the coffea framework that I noticed in running over a large dataset. The input is a simple TTree (all branches are basic types). The memory consumption of the python process is steadily increasing with each iteration of `processor.ProcessorABC.process` until it is fully filled up. While trying to reproduce this in a simple example, I've noticed that the problem is currelated with a larger number of baskets.

I've prepared a demonstrative MRE in my GitHub. It creates a simple TTree (100M events, 10 or 10k baskets, 3 branches of floats) and then processes it in different ways.

- `ptest.py` creates a `processor.ProcessorABC` and uses `run_uproot_job`+`iterative_executor`
- `ftest.py` calls `NanoEventsFactory.from_root` multiple times
- `utest.py` uses `uproot.iterate`

The observations are:
- `utest.py` is fine. So this is not an uproot problem.
- `ftest.py` is fine. So everything is cleaned up once a file is closed.
- `ptest.py` has memory usage slowly increasing (up to 1GiB) at every call to `process`. Then it drops. According the `tracemalloc`, the following package is responsible for most of it:
```
/home/runner/work/mre-coffea-memory/mre-coffea-memory/.venv/lib/python3.8/site-packages/uproot/source/file.py:67: size=858 MiB, count=30, average=28.6 MiB
```

For my actual application, the tracemalloc shows the following top 10 memory users. The compression is slowly growing in each call to `processor.ProcessorABC.process`.
```
[ Top 10 ]
/global/u2/k/kkrizka/lowmu/coffea_plots/.venv/lib/python3.9/site-packages/uproot/compression.py:442: size=27.7 GiB, count=4335, average=6699 KiB
/global/u2/k/kkrizka/lowmu/coffea_plots/.venv/lib/python3.9/site-packages/uproot/interpretation/library.py:76: size=4543 MiB, count=23804, average=195 KiB
/global/u2/k/kkrizka/lowmu/coffea_plots/.venv/lib/python3.9/site-packages/coffea/nanoevents/mapping/base.py:104: size=4543 MiB, count=23804, average=195 KiB
/global/u2/k/kkrizka/lowmu/coffea_plots/.venv/lib/python3.9/site-packages/coffea/hist/hist_tools.py:1082: size=2600 MiB, count=11903, average=224 KiB
/global/u2/k/kkrizka/lowmu/coffea_plots/.venv/lib/python3.9/site-packages/uproot/model.py:753: size=170 MiB, count=2365002, average=75 B
/global/u2/k/kkrizka/lowmu/coffea_plots/.venv/lib/python3.9/site-packages/uproot/source/cursor.py:48: size=127 MiB, count=2564484, average=52 B
/global/u2/k/kkrizka/lowmu/coffea_plots/.venv/lib/python3.9/site-packages/uproot/model.py:807: size=122 MiB, count=760232, average=168 B
/global/common/software/nersc/cori-2022q1/sw/python/3.9-anaconda-2021.11/lib/python3.9/json/decoder.py:353: size=101 MiB, count=1263487, average=84 B
/global/u2/k/kkrizka/lowmu/coffea_plots/.venv/lib/python3.9/site-packages/uproot/source/cursor.py:118: size=99.0 MiB, count=1533798, average=68 B
```

This can also be reproduced by running on an CMS Open Data MiniAOD multiple times.
```
python ptest.py $(printf '/data/kkrizka/opendata/cms/Run2015D/SingleMuon/MINIAOD/16Dec2015-v1/0034202D-A3A8-E511-BA9C-00259073E3DA.root %.0s' {1..10})
```

Last being:
```
--- [ Top 5 ] --- (total: 450592678)
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.9/site-packages/uproot/compression.py:93: size=58.8 MiB, count=18, average=3343 KiB
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.9/site-packages/uproot/model.py:753: size=44.7 MiB, count=607619, average=77 B
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.9/site-packages/uproot/source/cursor.py:48: size=37.1 MiB, count=748696, average=52 B
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.9/site-packages/uproot/model.py:807: size=29.8 MiB, count=185920, average=168 B
/usr/lib/python3.9/json/decoder.py:353: size=29.0 MiB, count=362249, average=84 B
--- [ Top 5 ] --- (total: 500308957)
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.9/site-packages/uproot/compression.py:93: size=65.3 MiB, count=20, average=3343 KiB
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.9/site-packages/uproot/model.py:753: size=49.6 MiB, count=675133, average=77 B
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.9/site-packages/uproot/source/cursor.py:48: size=41.3 MiB, count=831884, average=52 B
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.9/site-packages/uproot/model.py:807: size=33.1 MiB, count=206578, average=168 B
/usr/lib/python3.9/json/decoder.py:353: size=32.2 MiB, count=402491, average=84 B
```

The can be run as follows:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -f requirements.txt
python create_input.py example.root 100000000 10000
python ptest.py example.root # or any of the other scripts
```
