#  Copyright 2022 National Technology & Engineering Solutions of Sandia, LLC
#  (NTESS).  Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
#  Government retains certain rights in this software.
#
#  Redistribution and use in source and binary/rendered forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#   2. Redistributions in binary/rendered form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#   3. Neither the name of the copyright holder nor the names of its contributors
#      may be used to endorse or promote products derived from this software
#      without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This script calculates some function statistics intended to
# support bottom up analysis of functions in a binary.
#@author Nasser Salim
#@category Analysis
#@keybinding
#@menupath
#@toolbar

from ghidra.app.tablechooser import AddressableRowObject
from ghidra.app.tablechooser import StringColumnDisplay
from ghidra.program.util import CyclomaticComplexity

class FunctionStatRow(AddressableRowObject):

    def __init__(self, f):
        self.f = f
        self.callers = len(self.f.getCallingFunctions(monitor))
        self.calls = len(self.f.getCalledFunctions(monitor))
        self.size = sum([x.length for x in self.f.getBody()])
        self.complexity = CyclomaticComplexity().calculateCyclomaticComplexity(f, monitor)

    def getAddress(self):
        return self.f.getEntryPoint()

class NameCol(StringColumnDisplay):

    def getColumnName(self):
        return "Name"

    def getColumnValue(self, row):
        return row.f.getName()

class IntColumnDisplay(StringColumnDisplay):
    def getIntValue(self, row):
        raise NotImplementedError()

    def getColumnValue(self, row):
        return str(self.getIntValue(row))

    # cmp function for python 2 and 3
    def compare(self, row1, row2):
        a = self.getIntValue(row1)
        b = self.getIntValue(row2)
        return (a > b) - (a < b)

class CalledByCol(IntColumnDisplay):

    def getColumnName(self):
        return "CalledBy"

    def getIntValue(self, row):
        return row.callers

class CallsCol(IntColumnDisplay):

    def getColumnName(self):
        return "Calls"

    def getIntValue(self, row):
        return row.calls

class SizeCol(IntColumnDisplay):

    def getColumnName(self):
        return "Size"

    def getIntValue(self, row):
        return row.size

class ComplexCol(IntColumnDisplay):

    def getColumnName(self):
        return "Complexity"

    def getIntValue(self, row):
        return row.complexity

class TupleColumnDisplay(StringColumnDisplay):
    def getTupleValue(self, row):
        raise NotImplementedError()

    def getColumnValue(self, row):
        return str(self.getTupleValue(row))

    # cmp function for python 2 and 3
    def compare(self, row1, row2):
        a = self.getTupleValue(row1)
        b = self.getTupleValue(row2)
        return (a > b) - (a < b)

class InterestingCol(TupleColumnDisplay):

    def getColumnName(self):
        return "Interesting"

    def getTupleValue(self, row):
        # It would be weird if a function has more than 10^5 calls right?
        MAX_CALLS = 10**5
        return (MAX_CALLS-row.calls, row.size)

tcd = createTableChooserDialog("Function Statistics for Bottom-Up Analysis", None)

tcd.addCustomColumn(NameCol())
tcd.addCustomColumn(CalledByCol())
tcd.addCustomColumn(CallsCol())
tcd.addCustomColumn(SizeCol())
tcd.addCustomColumn(ComplexCol())
tcd.addCustomColumn(InterestingCol())

fm = currentProgram.getFunctionManager()
[tcd.add(FunctionStatRow(f)) for f in fm.getFunctionsNoStubs(True)]

tcd.show()
