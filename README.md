# sharepg - analysing shared regions in pangenomes

> [!NOTE]\
> Want to contribute? Feel free to open a PR on an issue about a missing, buggy or incomplete feature!

# Purpose

Tool to analyse shared sequences between populations in pangenomes. This small command-line tool aims to check regions in a graph that are shared by a collection of genomes, and that are not traversed by another collection.

It can extract:
+ Nodes that matches a criterion
+ Genomic intervals on each sequences
+ Bubbles with intervals

> [!NOTE]\
> Bubbles detection is made possible thanks to [BubbleGun](https://github.com/fawaz-dabbaghieh/bubble_gun), Fawaz Dabbaghie, Jana Ebler, Tobias Marschall, BubbleGun: enumerating bubbles and superbubbles in genome graphs, Bioinformatics, Volume 38, Issue 17, September 2022, Pages 4217–4219, https://doi.org/10.1093/bioinformatics/btac448

# Available commands

# Installation

Installation is made using `pip` with the provided `setup.py` file.

```bash
git clone https://github.com/Tharos-ux/sharepg.git
git pull
pip install --upgrade pip
python -m pip install .
```

Once installed, command-line become available out-of-the-box. You can check everything went well by printing the manpage with `sharepg -h`.

# Usage

Let's assume you happen to have:
+ a GFA graph, uncompressed or not
+ a list A of paths/walks names you want to follow (g0, g1, g2)
+ a list B of paths/walks names you want to avoid (g3, g4)
+ a reference name (g0)
+ you want to strictly have all paths/walks you follow and not any of the ones you want to avoid (threshold=1.)

```bash
# Extract nodes
sharepg disnodes graph.gfa -a g0 g1 g2 -b g3 g4 -r g0 -t 1 > disnodes.log
# Extract intervals
sharepg disintervals graph.gfa -a g0 g1 g2 -b g3 g4 -r g0 -t 1 > disintervals.log
# Extract bubbles
sharepg disbubbles graph.gfa -a g0 g1 g2 -b g3 g4 -r g0 -t 1 > disbubbles.log
```

> [!NOTE]\
> Threshold parameter is a float within range 0. to 1.; it represents the minimum proportion of genomes that needs to be in A and in the observed region and 1-threshold maximum proportion of genomes of B that can go through this same region. For instance, a threshold of 1. says that for a segment to be selected it needs to have all genomes of A and no genomes from B. A threshold of .7 says that at least 70% of A must go through the region and at most 30% of B can go through he region for it to be selected.
