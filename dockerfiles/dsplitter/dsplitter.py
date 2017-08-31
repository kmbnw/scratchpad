import os
import sys
import codecs
import math
from argparse import ArgumentParser

def mk_filename(outdir, idx):
    return open(os.path.join(outdir, 'split%05d' % (idx, )))


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--indir', required=True)
    p.add_argument('--outdir', required=True)
    p.add_argument('--encoding', default='UTF8')
    p.add_argument('--num-splits', required=True, type=int)

    args = p.parse_args()

    if args.num_splits < 2:
        p.error('--num-splits must be greater than 1')

    count = 0
    with codecs.open(args.input, 'r', encoding='UTF8') as ifh:
        for line in ifh:
            count += 1

    n_per_chunk = int(math.ceil(1.0 * count / args.num_splits))

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)


    def ensure_dir(file_idx):
        dname = os.path.join(args.outdir, 'part_%d' % (file_idx, ))
        if not os.path.exists(dname):
            os.makedirs(dname)
        return dname


    def mk_filename(file_idx):
        return os.path.join(ensure_dir(file_idx), 'split_output.txt')


    idx = [-1]
    def open_new_output_file():
        try:       
            close(mk_filename(idx[0]))
        except Exception:
            pass

        idx[0] += 1
        dst = mk_filename(idx[0])
        print (dst)
        if os.path.exists(dst):
            raise Exception('Refusing to overwrite %s' % (dst, ))
        return codecs.open(dst, 'w', encoding=args.encoding)


    for fname in os.listdir(args.indir):
        src = os.path.join(args.indir, fname)
        if not os.path.isfile(src):
            raise Exception(
                "Input directory must have only files; found subdirectory '%s'" %
                (src, ))

        idx[0] = -1
        dst = open_new_output_file()
        count = 0
        with codecs.open(args.input, 'r', encoding=args.encoding) as ifh:
            for line in ifh:
                dst.write(line)

                count += 1
                if count % n_per_chunk == 0:
                    count = 0
                    dst = open_new_output_file()
