import os
import sys
import codecs
import re
from argparse import ArgumentParser

_path_re = re.compile('^part_\\d+')

def mk_filename(outdir, idx):
    return open(os.path.join(outdir, 'split%05d' % (idx, )))


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--indir', required=True)
    p.add_argument('--outdir', required=True)
    p.add_argument('--encoding', default='UTF8')

    args = p.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    parts = {}
    def get_dirmap():
        dirs = os.listdir(args.indir)
        dirs = [d for d in dirs if os.path.isdir(os.path.join(args.indir, d))]
        for d in dirs:
            if not _path_re.match(d):
                raise Exception("Directory %s does not start with part_" % (d, ))
            idx = int(d.split('/')[0].split('_')[1])
            if idx in parts:
                raise Exception("Already found part %d: %s" % (idx, parts[idx]))
            parts[idx] = d
        expected = list(range(0, len(parts)))
        actual = list(sorted(parts.keys()))
        if actual != expected:
            raise Exception(
                "part_ directories must be sequentially numbered; got %s but expected %s" %
                (actual, expected))

        if not 0 in parts:
            raise Exception("First directory must be indexed at zero")

        return parts

    dirmap = get_dirmap()
    seen = set()

    # for each file in each part directory, append the output
    for idx in sorted(dirmap):
        parent_dir = os.path.join(args.indir, dirmap[idx])
        fnames = os.listdir(parent_dir)
        fnames = [f for f in fnames if os.path.isfile(os.path.join(parent_dir, f))]

        for fname in fnames:
            src = os.path.join(parent_dir, fname)
            dst = os.path.join(args.outdir, fname)
            print (dst)

            if idx == 0:
                seen.add(fname)
            elif fname not in seen:
                raise Exception("File '%s' from part_%d not seen in part_0" % (fname, idx))

            with codecs.open(dst, 'a', encoding='UTF8') as ofh:
                with codecs.open(src, 'r', encoding='UTF8') as ifh:
                    for line in ifh:
                        ofh.write(line)
