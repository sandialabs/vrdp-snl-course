#!/usr/bin/python3
"""
This was inspired by the 'calltree' python package available at
   https://github.com/vadivelmurugank/calltree
"""

import re
import os
import shlex
import subprocess
import argparse
import json
from collections import defaultdict

class TermOutput(object):

    class TermCol(object):
        def __init__(self, name, key, just):
            self.name = name
            self.key = key
            self.just = just
            self.size = len(name)

    def __init__(self):
        self.cols = []

    def addCol(self, name, key, just="l"):
        if just.lower() in ["r", "right"]:
            just = ">"
        elif just.lower() in ["l", "left"]:
            just = "<"
        elif just.lower() in ["c", "center"]:
            just = "^"
        else:
            raise ValueError("Unknown justify specificier {}.".format(just))
        self.cols.append( TermOutput.TermCol(name, key, just) )

    @staticmethod
    def max_str(data, key, minlen=0):
        maxlen = minlen
        for row in data:
            elt = row[key]
            thislen = len(str(elt))
            if thislen > maxlen:
                maxlen = thislen
        return maxlen

    def print(self, data):
        for col in self.cols:
            if col.key is not None:
                col.size = TermOutput.max_str(data, col.key, len(col.name))

        fmt = ("{:{}{}} "*len(self.cols)).rstrip()

        outrow = []
        for col in self.cols:
            outrow.extend([col.name, col.just, col.size])
        print(fmt.format(*outrow))

        for row in data:
            outrow = []
            for col in self.cols:
                if col.key is not None:
                    outrow.extend([row[col.key], col.just, col.size])
                else:
                    outrow.extend(["", col.just, col.size])
            print(fmt.format(*outrow))


def memoize_funcdef(f):
    """ Too many people try to make a general memoization solution. This one
        works for the FunctionDef class.
    """
    memo = {}
    def helper(*args):
        key = args[0]
        if key not in memo:
            memo[key] = f(*args)
        return memo[key]
    return helper

@memoize_funcdef
class FunctionDef(object):
    """ This is a container for a function definition.  """

    def __init__(self, name, sourcefile, line, definition, callers, callees):
        self.name = name
        self.sourcefile = sourcefile
        self.line = line
        self.definition = definition
        self.callers = callers
        self.callees = callees

    def __repr__(self):
        return "{} ({}:{})".format(self.name, self.sourcefile, self.line)

    def __hash__(self):
        return hash(self.name)

    def json(self):
        return [self.name, self.sourcefile, self.line]

class CscopeParser(object):

    def __init__(self, sourcedb=None, filesdb=None, verbose=False, debug=False):
        """ document tested """
        self.debug = debug
        self.verbose = verbose
        self.funcs = {}
        # Try the cwd and default file name
        if sourcedb is None:
            self.dprint("Looking for default cscope.out file.")
            sourcedb = "cscope.out"
        if not os.path.exists(sourcedb):
            raise FileNotFoundError("Invalid sourcedb path: {}".format(sourcedb))
        self.sourcedb = os.path.abspath(sourcedb)

        if filesdb:
            if not os.path.exists(filesdb):
                raise FileNotFoundError("Invalid filesdb path: {}".format(filesdb))
            self.filesdb = os.path.abspath(filesdb)
        else:
            filesdb = "cscope.files"
            # try the same directory as the sourcedb
            same_as_sourcedb = os.path.join(os.path.dirname(sourcedb), filesdb)
            if os.path.exists(same_as_sourcedb):
                self.filesdb = os.path.abspath(same_as_sourcedb)
            # or try the current working directory
            elif os.path.exists(filesdb):
                self.filesdb = os.path.abspath(filesdb)
            # Otherwise use recursive search
            else:
                self.filesdb = None

    def dprint(self, msg):
        if self.debug:
            print(msg)

    def warn(self, msg):
        if self.verbose:
            print("Warning: {}".format(msg))

    def run_cscope(self, level, pattern):
        """ Handle the external call to cscope and the parsing of output. """
        if self.filesdb:
            files = "-i {}".format(self.filesdb)
            self.dprint("Using {} as files.".format(self.filesdb))
        else:
            files = "-R"
            self.dprint("Using recursive search for files.")
        # Construct the command to cscope
        command = "cscope -f {} {} -L -{} {}".format(self.sourcedb, files, level, shlex.quote(pattern))
        self.dprint(command)
        cmdstr = shlex.split(command)

        proc = subprocess.Popen(cmdstr, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        outstr,errstr=proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError("Call to cscope failed.  STDERR is: \n{}".format(errstr))
        # comes out as filename, func, line, define
        return [line.split(' ', 3) for line in outstr.strip().split('\n') if line.count(' ') >= 3]

    def add_func_def(self, func):
        """ Use cscope to get the function definition, store it in the parser dictionary, and return it. """
        defdata = self.run_cscope(1,func)

        if len(defdata) == 0:
            self.warn("Cannot locate definition for {}.".format(func))
            return None

        keep = []
        for d in defdata:
            # Skip external defs
            if d[0].startswith("/"):
                self.warn("Skipping external definition for {} in {}.".format(func, d[0]))
                continue
            keep.append(d)

        if len(keep) == 0:
            return None # they were all external
        else:
            defdata = keep

        if len(defdata) > 1:
            self.warn("Duplicate definitions found for {}. Dropping all but one.".format(func))

        callers = len(self.run_cscope(3, func))
        callees = len(self.run_cscope(2, func))

        fd = FunctionDef(defdata[0][1], defdata[0][0], defdata[0][2], defdata[0][3], callers, callees)
        self.funcs[fd.name] = fd
        return fd

    def get_functions(self, pattern=".*"):
        """ Using the union of all forward and backward slices, gather all function
            definitions matching the given pattern.
        """
        # Let python do the matching in this case.
        all_func_names =  set([x[1] for x in self.run_cscope(2, ".*") if re.match(pattern, x[1])])
        all_func_names.update([x[1] for x in self.run_cscope(3, ".*") if re.match(pattern, x[1])])
        defs = []
        for func in sorted(all_func_names):
            fd = self.add_func_def(func)
            if fd:
                defs.append(fd)
        return defs

    def get_stats(self, pattern=".*"):
        self.get_functions(pattern)
        return [[f.name, f.sourcefile, f.line, f.definition, f.callers, f.callees]
                for f in self.funcs.values()]

def get_argparse():

    parser = argparse.ArgumentParser(description='Run cscopeparse on the given project.')
    parser.add_argument("-d", "--db", action="store", type=str, dest="sourcedb",
                        help="location of the cscope database (cscope.out)")
    parser.add_argument("-f", "--files", action="store", type=str, dest="filesdb",
                        help="location of the cscope files list (cscope.files)")
    parser.add_argument("-l", "--list", action="store_true", dest="list",
                        help="Only list all functions indexed by cscope")
    parser.add_argument("-j", "--json", action="store_true", dest="json",
                        help="Return data as json")
    parser.add_argument("-s", "--sort", action="store", dest="sort", choices=["callers", "callees"],
                        default="callers", help="Which stat to sort by.")
    parser.add_argument("-r", "--reverse", action="store_true", dest="reverse",
                        help="Reverse the sorting behavior.")
    parser.add_argument("-p", "--pattern", action="store", type=str, dest="pattern", default=".*",
                        help="Filter results by the given pattern.")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                        help="Display more output and warnings.")
    parser.add_argument("--debug", action="store_true", dest="debug",
                        help="Debug this script.")
    return parser

def main():

    parser = get_argparse()
    args = parser.parse_args()
    csp = CscopeParser(args.sourcedb, verbose=args.verbose, debug=args.debug)

    if args.list:
        funcs = csp.get_functions(args.pattern)
        funcs.sort(key=lambda f: f.name)
        if args.json:
            print(json.dumps([f.json() for f in funcs]))
        else:
            for f in funcs:
                print(f)
    else:
        stats = csp.get_stats(args.pattern)
        if args.json:
            print(json.dumps(stats))
        else:
            if args.sort == "callees":
                stats.sort(reverse=not args.reverse, key=lambda x: x[5])
            else:
                stats.sort(reverse=not args.reverse, key=lambda x: x[4])

            out = TermOutput()
            out.addCol("FUNCTION", 0)
            out.addCol("FILE", 1)
            out.addCol("LINE", 2, "r")
            out.addCol("CALLERS", 4, "r")
            out.addCol("CALLEES", 5, "r")
            out.print(stats)

if __name__ == "__main__":
    main()
