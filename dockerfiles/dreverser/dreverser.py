import os
import sys
import codecs
import math
from argparse import ArgumentParser

if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--indir', required=True)
    p.add_argument('--outdir', required=True)
    p.add_argument('--encoding', default='UTF8')

    args = p.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    for fname in os.listdir(args.indir):
        src = os.path.join(args.indir, fname)
        if not os.path.isfile(src):
            raise Exception(
                "Input directory must have only files; found subdirectory '%s'" %
                (src, ))

        dst = os.path.join(args.outdir, fname)
        if os.path.exists(dst):
            raise Exception("Cowardly refusing to overwrite '%s'" % (dst, ))

        with codecs.open(src, 'r', encoding=args.encoding) as ifh:
            with codecs.open(dst, 'w', encoding=args.encoding) as ofh:
                for line in ifh:
                    line = ''.join(reversed(line))

                    ofh.write(line)
