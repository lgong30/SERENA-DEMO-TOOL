"""PDF Builder"""
from subprocess import Popen, PIPE, STDOUT
import os
import os.path
from sys import platform as _platform
from send2trash import send2trash

# copied fomr Latextools
DEFAULT_COMMAND_LATEXMK = ["latexmk", "-cd", "-f", "-pdf",
					"-interaction=nonstopmode", "-synctex=1"]

DEFAULT_COMMAND_WINDOWS_MIKTEX = ["texify", "-b", "-p", "--engine=pdftex",
					"--tex-option=\"--synctex=1\""]
DEFAULT_INTERMEDIATE_FILE_EXTS = {'.aux', '.lof', '.log', '.lot', '.fls', '.out', '.toc', '.fdb_latexmk', '.synctex.gz',
                                  '.pdfsync', '.gz'}

class PDFBuilder(object):
    """Simple PDF Builder"""

    def __init__(self, tex_file_list, **kwargs):
        super(PDFBuilder, self).__init__()
        self.tex_file_list = tex_file_list
        self.tex_dir = kwargs.get('tex_dir', os.getcwd())
        self.output_dir = kwargs.get('output_dir', os.getcwd())
        self.options = ""
        self.display_all = kwargs.get('display', False)
        self.temp_file_exts = kwargs.get('temp_file_exts', DEFAULT_INTERMEDIATE_FILE_EXTS)
        if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
            self.command = DEFAULT_COMMAND_LATEXMK
            self.options = ["--output-directory=%s" % self.output_dir]

        elif _platform == "win32":
            self.command = DEFAULT_COMMAND_WINDOWS_MIKTEX
            self.options = ["--tex-option=\"" + ("--output-directory=%s" % self.output_dir) + "\""]
        else:
            print("Unknown platform %s" % _platform)
            self.command = None

        self.make_directory(self.output_dir)


    def make_directory(self, directory):
        """Make directory

        Args:
            directory: name of directory to be made
        """
        if not os.path.exists(directory):
            try:
                print("Making directory %s" % directory)
                os.makedirs(directory)
            except OSError as msg:
                print("Failed to create directory %s, because %s" % (directory, str(msg)))
                return




    def make_pdfs(self):
        """Make PDFs"""
        if self.command is None:
            print("Make PDF failed, because the platform (i.e., %s) is not supported" % _platform)
            return

        for tex_file in self.tex_file_list:
            full_tex_file = os.path.join(self.tex_dir, tex_file)
            cmd = self.command + self.options + [full_tex_file]
            print ("Run command '%s'" % (" ".join([str(s) for s in cmd])))
            p = Popen(
                cmd,
                stdout=PIPE,
                stderr=PIPE
            )
            stdout, stderr = p.communicate()
            if self.display_all:
                print ("%s %s" % (stdout, stderr))
            else:
                print ("%s" % stderr)

    def clean(self):
        """Clean output directory"""
        for f in os.listdir(self.output_dir):
            name, ext = os.path.splitext(f)
            if ext in self.temp_file_exts:
                print("Move {} to trash".format(f))
                send2trash(os.path.join(self.output_dir, f))
        


if __name__ == "__main__":
    pdf_bulder = PDFBuilder(tex_file_list=["arrival_matching.tex", "previous_matching.tex"],
                            tex_dir=os.path.abspath("./outputs"),
                            output_dir=os.path.abspath("./pdfs"))
    pdf_bulder.make_pdfs()
    pdf_bulder.clean()





