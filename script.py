#!/usr/bin/python
"""

EXAMPLE USE:
time python $HOME/split_sample_matrix_by_attribute/script.py attr_fname=$HOME/gse15745/GSE15745.GPL6104.mRNA.normed.tab.npy_vs_GSE15745.GPL8490.methyl.normed.tab.npy.coltitles.samples.txt npy_fname=$HOME/gse15745/old/GSE15745.GPL6104.mRNA.normed.tab.npy_aligned_with_GSE15745.GPL8490.methyl.normed.tab.npy.npy
"""
import numpy as np
import sys


def split_M(attr_row, M):
  assert len(attr_row) == np.size(M,1), "len(attr_row)%d == np.size(M,1)%d" % (len(attr_row), np.size(M,1))
  attr_idxs = map_attr_row(attr_row)
  return dict([(s, M[:,d]) for s, d in attr_idxs.items()])

def map_attr_row(attr_row):
  attrs = list(sorted(set(attr_row)))
  attr_idxs = dict([ (s, []) for s in attrs])
  for i, s in enumerate(attr_row):
    attr_idxs[s].append(i)
  return attr_idxs

def ma_to_txt(M, fname, delimiter="\t", format="%.6f"):
  fp = open(fname, "w")
  for row in M:
    s = []
    for i in range(np.size(M,1)):
      if row.mask[i]:
        s.append("")
      else:
        s.append(format%row.data[i])
    fp.write(delimiter.join(s))
    fp.write('\n')
  fp.close()

  
def main(attr_fname=None, npy_fname=None, to_txt=True):
  print "Loading %s..." % attr_fname
  attr_row = open(attr_fname).read().strip().split(',')
  print "Loading %s..." % npy_fname
  M = np.ma.load(npy_fname)
  D = split_M(attr_row, M)
  print "%d unique attributes in list of %d attributes" % (len(D), len(attr_row))
  print "Attributes:", " ".join(D.keys())
  print "Column sizes", " ".join(map(str, [np.size(x,1) for x in D.values()]))
  print "Row sizes (should be all equal)", " ".join(map(str, [np.size(x,0) for x in D.values()]))
  # Dump matrices to disk
  print "Writing matrices to disk..."
  for name, Q in D.items():
    fname = npy_fname+".%s.npy" % name
    print "Saving %s..." % fname
    np.ma.dump(Q, fname)
  if to_txt:
    print "Output matrices to text.\n====="
    for name, Q in D.items():
      fname = npy_fname+".%s.npy.tab" % name
      print "Saving %s..." % fname
      ma_to_txt(Q, fname)

if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
