# Visual Demonstration Generator for SERENA

This repository implements a simple tool for creating visual demonstration for a crossbar scheduling algorithm -- [SERENA][1]. 

## Installation

Under development 

## Usage (Linux or Mac)

### Install Dependencies

```bash
pip3 install -r requirements.txt
```

Note that, you might need add `sudo` (i.e., `sudo pip3 install -r requirements.txt`) to solve **permission denied** issue.

### Run


```bash
usage: serena_demo_ctl [-?]
                       {gen_matchings,gen_matchings_from_txt,merge_two_matchings,shell,runserver}
                       ...

positional arguments:
  {gen_matchings,gen_matchings_from_txt,merge_two_matchings,shell,runserver}
    gen_matchings       Generate (random) matchings
    gen_matchings_from_txt
                        Generate matchings from a TXT file
    merge_two_matchings
                        Merge Two Matchings
    shell               Runs a Python shell inside Flask application context.
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit
```

#### Generate Two Matchings & Merge Them

```bash
usage: serena_demo_ctl gen_matchings [-?] [--position {0,1}] [--size SIZE]
                                     [--minWeight MIN_WEIGHT]
                                     [--maxWeight MAX_WEIGHT]
                                     [--SolveIt {N,R,S}] --output-dir
                                     OUTPUT_DIR

Generate (random) matchings

optional arguments:
  -?, --help            show this help message and exit
  --position {0,1}, -p {0,1}
                        OPTIONAL: weight position Default: 0, i.e., left.
  --size SIZE, -s SIZE  OPTIONAL: matching size Default: 8.
  --minWeight MIN_WEIGHT, -w MIN_WEIGHT
                        OPTIONAL: minimum weight on each edge Default: 0.
  --maxWeight MAX_WEIGHT, -W MAX_WEIGHT
                        OPTIONAL: maximum weight on each edge Default: 100.
  --SolveIt {N,R,S}, -S {N,R,S}
                        OPTIONAL: Merge the two matchings with certain default
                        choice when tie occurs N: do not solve R: solve with
                        default choice R S: solve with default choice S
                        Default: N.
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory
```

#### Examples 

Under construction


## Usage (on Windows)

Under development


















[1]: P. Giaccone, B. Prabhakar and D. Shah, "Randomized scheduling algorithms for high-aggregate bandwidth switches," in IEEE Journal on Selected Areas in Communications, vol. 21, no. 4, pp. 546-559, May 2003.
doi: 10.1109/JSAC.2003.810496.

