#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from getopt import getopt
import sys

class FilterComments:

    comment_types = {
        'Haskell' : ['---\n', '-- '],
        'Shell' : ['##\n', '# '],
        'Lisp' : [';;;\n', '; '],
        'Java' : ['///\n', '// '],
        'C' : ['/**\n', ' * ']
    }

    flags = 'hksljco:'

    full_flags = ['help', 'haskell-style', 'shell-style', 'lisp-style',
                  'java-style', 'c-style', 'output=']

    def __init__(self, args):
        self.args = args
        self.style = self.comment_types['C']
        self.output = None

    def print_help(self):
        print(self.args[0] + " -[flags]o [output] [inputs]")
        print("Flags include: ")
        print("")
        print("  -h, --help:")
        print("    Gives this help screen.")
        print("  -k, --haskell-style")
        print("    Uses haskell style comments.")
        print("  -s, --shell-style")
        print("    Uses shell style comments.")
        print("  -l, --lisp-style")
        print("    Uses lisp style comments.")
        print("  -j, --java-style")
        print("    Uses java (C++ single line comments) style comments.")
        print("  -c, --c-style")
        print("    Uses c style comments.")
        print("  -o, --output")
        print("    Sets output file, if none defaults to stdout.")
        print("")

    def parse_arguments(self):
        sorted_args, self.inputs = getopt(self.args[1:], self.flags, self.full_flags)
        for pair in sorted_args:
            if pair[0] == '--haskell-style' or pair[0] == '-k':
                self.style = self.comment_types['Haskell']
            elif pair[0] == '--shell-style' or pair[0] == '-s':
                self.style = self.comment_types['Shell']
            elif pair[0] == '--lisp-style' or pair[0] == '-l':
                self.style = self.comment_types['Lisp']
            elif pair[0] == '--java-style' or pair[0] == '-j':
                self.style = self.comment_types['Java']
            elif pair[0] == '--c-style' or pair[0] == '-c':
                self.style = self.comment_types['C']
            elif pair[0] == '--output' or pair[0] == '-o':
                self.output = pair[1]
            elif pair[0] == '--help' or pair[0] == '-h':
                self.print_help()
                sys.exit()

    def filter_line(self, line, file_buffer, in_comment):
        if not in_comment:
            if line == self.style[0]:
                in_comment = True
        else:
            if line[:len(self.style[1])] == self.style[1]:
                file_buffer += line[len(self.style[1]):]
            else:
                file_buffer += '\n'
                in_comment = False
        return file_buffer, in_comment

    def filter_comments(self):
        in_comment = False
        if self.output == None:
            output_file = sys.stdout
        else:
            output_file = open(self.output, 'a')
        file_buffer = '\n'

        for filename in self.inputs:
            try:
                input_file = open(filename, 'r')
            except FileNotFoundError:
                print("An input file has not been found.", file = sys.stderr)
                sys.exit()
            for line in input_file.readlines():
                file_buffer, in_comment = self.filter_line(
                    line,
                    file_buffer,
                    in_comment)
            input_file.close()

        output_file.write(file_buffer)
        output_file.close()

def main(args = sys.argv):
    if len(args) < 2:
        print("Need more arguments.", file = sys.stderr)
        sys.exit()
    app = FilterComments(args)
    app.parse_arguments()
    app.filter_comments()

if __name__ == '__main__':
    main()

# vim: set ts=8 sts=4 sw=4 et:
