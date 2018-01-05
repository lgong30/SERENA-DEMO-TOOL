import os.path
import os
from util import make_directory, path_split
from auto_matching import get_tex_doc, gen_tex_file
from auto_cycle import make_tex_doc
import time



class TexBuilderBase(object):
    """Base class for TeX builder"""
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.tex_file_list = []

    def make_tex(self, overwrite_handler):
        raise NotImplementedError  # abstract

    def get_tex_files(self):
        """Returns generated TeX files (in a list)"""
        if len(self.tex_file_list) == 0:
            # make tex files (no overwriting)
            return self.make_tex(overwrite_handler=lambda fn: False)
        else:
            return self.tex_file_list


class MatchingTeXBuilder(TexBuilderBase):
    """Generate TeX file"""
    def __init__(self, matching_list, output_dir, **kwargs):
        """Constructor for TeXBuilder

        Args:
            matching_list: 2d-list, list for matchings, where each matching is
                           represented by a 1d-list. Inside the tuple,
                           there are two elements: the first describes
                           the edges and weights in the matchings in terms of
                           a dict with keys 'i' (in), 'o' (out), 'w' (weight),
                           the second gives name for matching. TODO
            output_dir: str, where to store the resulted TeX files
            TeX_template: str, list of str or None, where is the template files, if
                          no template is provided, the default one will be used. If
                          str type is provided, all matchings will use the same template.
                          If a list is provided, it should have the same length as
                          matching_list.
                          Frankly speaking the type of this argument
                          is not well-designed (not quite flexible).
        """
        super(MatchingTeXBuilder, self).__init__(output_dir)
        self.matchings = matching_list
        # self.output_dir = output_dir
        # self.tex_file_list = []

        TeX_template = kwargs.get('tex_template', None)
        if TeX_template is None:
            self.templates = None
            self.position = kwargs.get('position', 0)
        elif isinstance(TeX_template, str) or isinstance(TeX_template, unicode):
            path, name = path_split(TeX_template)
            self.templates = [(path, name)] * len(self.matchings)
        else:
            if len(TeX_template) != len(self.matchings):
                print("TeX_template should have the same length as matching_list, "
                      "if it is also a list!")
                exit(1)
            self.templates = map(path_split, TeX_template)


    def make_tex(self, overwrite_handler):
        """Make TeX files

        Args:
            overwrite_handler: a function which accepts a single str argument,
                               that is used to handle overwritten issue.

        Returns:
                tex_file_list, if failed returning an empty list.
        """
        make_directory(self.output_dir)
        tex_file_list = []
        for i, m in enumerate(self.matchings):
            if self.templates is None:
                tex_doc = get_tex_doc(m[0], position=self.position)
            else:
                tex_doc = get_tex_doc(m[0], template_dir=self.templates[i][0],
                                      template=self.templates[i][1])
            counter = 0
            while not (gen_tex_file(tex_doc, filename=os.path.join(self.output_dir, m[1] + '.tex'),
                                    overwrite_handler=overwrite_handler)):
                if counter > 10:
                    print("Failed to create file for matching %s." % (str(m[0])))
                    return
                m[1] += time.strftime("_%H-%M-%S")
                counter += 1
            tex_file_list.append(m[1])
            print("Successfully create tex file {}".format(m[1]))
        self.tex_file_list = tex_file_list
        return tex_file_list

    # def get_tex_files(self):
    #     """Returns generated TeX files (in a list)"""
    #     if len(self.tex_file_list) == 0:
    #         # make tex files (no overwriting)
    #         return self.make_tex(overwrite_handler=lambda fn: False)
    #     else:
    #         return self.tex_file_list


class CycleTeXBuilder(TexBuilderBase):
    """TeX Builder for cycles"""
    def __init__(self, cycles, output_dir, **kwargs):
        super(CycleTeXBuilder, self).__init__(output_dir)
        self.cycles = cycles
        TeX_template = kwargs.get('tex_template', None)
        if TeX_template is None:
            self.templates = None
        elif isinstance(TeX_template, str) or isinstance(TeX_template, unicode):
            path, name = path_split(TeX_template)
            self.templates = [(path, name)] * len(self.cycles)
        else:
            if len(TeX_template) != len(self.cycles):
                print("TeX_template should have the same length as cycles, "
                      "if it is also a list!")
                exit(1)
            self.templates = map(path_split, TeX_template)

    def make_tex(self, overwrite_handler):
        make_directory(self.output_dir)
        tex_file_list = []
        for i, c in enumerate(self.cycles):
            if self.templates is None:
                tex_doc = make_tex_doc(**c[0])
            else:
                tex_doc = make_tex_doc(template_dir=self.templates[i][0],
                                      template=self.templates[i][1],
                                       **c[0])
            counter = 0
            while not (gen_tex_file(tex_doc, filename=os.path.join(self.output_dir, c[1] + '.tex'),
                                    overwrite_handler=overwrite_handler)):
                if counter > 10:
                    print("Failed to create file for cycle %s." % (str(c[0])))
                    return
                c[1] += time.strftime("_%H-%M-%S")
                counter += 1
            tex_file_list.append(c[1])
            print("Successfully create tex file {}".format(c[1]))
        self.tex_file_list = tex_file_list
        return tex_file_list





