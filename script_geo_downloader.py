#!/usr/bin/python
"""Split a matrix by columns according to some attribute.
Designed to be used with output from geo_downlaoder module.


EXAMPLE USE:
  python $HOME/split_sample_matrix_by_attribute/script_geo_downloader.py fname_tab=$HOME/gse15745_sept2012/GSE15745_GPL6104.normed.tab fname_samples=$HOME/gse15745_sept2012/GSE15745_GPL6104.samples.tab attr=characteristics_ch1:tissue
"""
import re

RX_CLEAN = re.compile('[^a-zA-Z0-9-_]')

class Samples(object):
  def __init__(self, fp):
    self.headers = []
    self.attrs = {}
    for line in fp:
      if len(line) >= 2 and line[:2] == "##":
        self.headers.append(line)
      elif len(line) >= 1 and line[0] == "#":
        name, c, row = line[1:].partition('\t')
        self.attrs[name] = row.rstrip('\n').split('\t')
      else:
        continue
        
def clean(s):
  return RX_CLEAN.sub('_', s.upper())

def main(fname_tab=None, fname_samples=None, attr=None):
  assert fname_tab and fname_samples and attr

  S = Samples(open(fname_samples))
  assert attr in S.attrs
  assert "accession" in S.attrs
  unique_attr_values = set(S.attrs[attr])
  n = S.attrs[attr]
  print "%d unique_attr_values (of %d total) for attribute %s: %s" % \
      (len(unique_attr_values), n, attr, ", ".join(unique_attr_values))
  value_cols = {}
  for v in unique_attr_values:
    value_cols[v] = []

  # Get column numbers for each unique value
  for i in xrange(n):
    value_cols[S.attrs[attr][i]].append(i)
  print "Attribute distributions:"
  for name, idxs in value_cols.items():
    print "%s: (%d) %s" % (name, len(idxs), ",".join([int(x) for x in sorted(idxs)]))
  i_to_attr = dict([(i, v) for v, i in value_cols.items()])

  # Save one copy of the matrix, one per attribute value
  fps = {}
  for v in unique_attr_values:
    outname = fname_tab+".%s=%s.tab" % (attr, v)
    fps[v] = open(outname, "w")
    print "Opened %s for writing..." % outname

  for line in open(fname_tab):
    row = line.rstrip('\n').split('\t')
    # Write row ID to all files.
    for fp in fps.values():
      fp.write(row[0])
    # Selectively write column values per file.
    for i, v in enumerate(row[1:]):
      fps[i_to_attr[i]].write("\t%s"%v)
    # Terminate line with newline in all files.
    for fp in fps.values():
      fp.write("\n")
  # Close all files
  for name, fp in fps.items():
    print "Closing file for %s..." % name
    
    
