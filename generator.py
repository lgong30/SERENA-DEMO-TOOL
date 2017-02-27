#! /usr/local/bin/python
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError as msg:
    print ("ImportError: %s" % msg)
    exit(1)
import os
try:
    import numpy as np
except ImportError as msg:
    print ("ImportError: %s" % msg)
    exit(1)
import argparse
import sys


# get options from command line
def get_opt():
    parser = argparse.ArgumentParser(description="BipartMatching Generator")
    parser.add_argument('-p', "--position", action="store", help="weight position", type=int, default=0)
    parser.add_argument('-s', "--size", action="store", help="matching size", type=int, default=8)
    parser.add_argument('-w', "--minWeight", action="store", help="minimum weight on each edge", type=int, default=0)
    parser.add_argument('-W', "--maxWeight", action="store", help="maximum weight on each edge", type=int, default=100)
    parser.add_argument('-f', "--file", action="store", help="custom data for a matching", type=str, default="")
    parser.add_argument('-c', "--consistency", action="store", help="consistent matching data from the same graph", type=str, default="")
    parser.add_argument('-o', "--output", action="store", help="output file name (for example, test.tex)", type=str, default="bm.tex")


    try:
        args = parser.parse_args(sys.argv[1::])
    except IOError as msg:
        parser.error(str(msg))
        exit(1)
    return args


# generate random matching
def gen_random_matching(N, min_weight=1, max_weight=50, check_file=None):
    def get(filename):
        import re 
        p = re.compile(r"^%\s(\d+)\s(\d+)\s(\d+)")
        m = {}
        with open(filename, 'r') as fp:
            for line in fp:
                e = re.findall(p, line)
                if len(e) > 0:
                    e = e[0]
                    m[e[:2]] = int(e[2])
        return m

    m = np.random.permutation(N).tolist()
    matching = []
    weights = np.random.randint(min_weight, high=max_weight, size=N)

    cons_matching = {}
    if not (check_file is None):
        cons_matching = get(check_file)
        # for debug
        # print cons_matching
 
    for i, o in enumerate(m):
        w = weights[i]
        e = (str(i + 1), str(o + 1))
        if e in cons_matching:
            # print ("$ same edge: %s use previous weight"
            w = cons_matching[e]
        matching.append({'i': i + 1, 'o': o + 1, 'w': w })
    return matching


# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def get_tex_doc(matching, **options):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    N = 8
    args = {'N': len(matching), 'matching': matching}
    args.update(options)
    return j2_env.get_template('matching_template.tex').render(
        args
    )


def gen_tex_file(tex_doc, filename="example.tex"):
    add_msg = "%% This file is generated by Jinja2"
    with open(filename, 'w') as texf:
        texf.write("%s\n" % add_msg)
        texf.write(tex_doc)


if __name__ == '__main__':
    args = get_opt()
    # print str(args)
    consistency = None
    if len(args.consistency) > 0:
        consistency = args.consistency


    matching = gen_random_matching(args.size, min_weight=args.minWeight, max_weight=args.maxWeight, check_file=consistency)
    # print matching
    doc = get_tex_doc(matching, position=args.position)
    gen_tex_file(doc, filename=args.output)

