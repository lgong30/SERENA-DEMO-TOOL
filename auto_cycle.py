"""Make TeX for a cycle
"""
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError as msg:
    print ("ImportError: %s" % msg)
    exit(1)
import os
import os.path
try:
    import numpy as np
except ImportError as msg:
    print ("ImportError: %s" % msg)
    exit(1)


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = u'cycle_template_flexible.tex'


def make_tex_doc(cycle, radius, node_size, **options):
    """Generate tex code for a cycle"""

    template_dir = options.get("template_dir", THIS_DIR)
    template_filename = options.get("template", DEFAULT_TEMPLATE)
    j2_env = Environment(loader=FileSystemLoader(template_dir),
                         trim_blocks=True)
    direction = options.get('direction', 0)
    args = {
        "nodes": cycle['nodes'],
        "edges": cycle['edges'],
        "radius": radius,
        "direction": direction,
        "node_size": node_size
    }

    args.update(options)

    return j2_env.get_template(template_filename).render(
        args
    )


# if __name__ == "__main__":
#     N = 8
#     R = (np.random.permutation(N).tolist(), dict(zip(range(N),
#         np.random.randint(1, high=10,size=N))))
#     S = (np.random.permutation(N).tolist(), dict(zip(range(N),
#         np.random.randint(1, high=10,size=N))))
#     print ("Random matching: %s" % str(R))
#     print ("Previous matching: %s" % str(S))
#     M, W, C = simple_merge(R, S, return_cycles=True)
#     for c in C:
#         cycle_info = format_cycle(c, N)
#         print make_tex_doc(**cycle_info)



    