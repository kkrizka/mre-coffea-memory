Tries to reproduce a memory leak in the coffea framework that I noticed in running over a large dataset. The input is a simple TTree (all branches are basic types). The memory consumption of the python process is steadily increasing with each iteration of `processor.ProcessorABC.process` until it is fully filled up.

This MRE tries to reproduce it in four examples. It is based on the coffea test sample (`nano_dy.root`), following [instructions from the documentation](https://coffeateam.github.io/coffea/notebooks/nanoevents.html). It scales the small `nano_dy.root` into a "large dataset" by looping over it multiple times.

There are three versions of the code:
- `ptest.py` creates a `processor.ProcessorABC` (based on `MyZPeak`) and uses `run_uproot_job`+`iterative_executor`
- `ftest.py` calls `NanoEventsFactory.from_root` multiple times
- `utest.py` uses `uproot.iterate`

The observations are:
- utest.py (uproot only, no coffea) memory usage is constant. So I don't think this is an uproot issue.
- Both ptest and ftest slowly grow with size. The main source of increase is the following.
```
/home/runner/work/mre-coffea-memory/mre-coffea-memory/.venv/lib/python3.8/site-packages/uproot/_util.py:564: size=5145 KiB (+51.4 KiB), count=75802 (+758), average=70 B
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


The can be run as follows:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -f requirements.txt
python ptest.py # or any of the other ones
```
