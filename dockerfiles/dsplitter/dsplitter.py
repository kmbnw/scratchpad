import os
import sys
import codecs
import math
from argparse import ArgumentParser

def chunk_size(src, encoding):
    count = 0
    with codecs.open(src, 'r', encoding=encoding) as ifh:
        for line in ifh:
            count += 1

    return int(math.ceil(1.0 * count / args.num_splits))


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--indir', required=True)
    p.add_argument('--outdir', required=True)
    p.add_argument('--encoding', default='UTF8')
    p.add_argument('--num-splits', required=True, type=int)

    args = p.parse_args()

    if args.num_splits < 2:
        p.error('--num-splits must be greater than 1')

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)


    def ensure_dir(file_idx):
        dname = os.path.join(args.outdir, 'part_%d' % (file_idx, ))
        if not os.path.exists(dname):
            os.makedirs(dname)
        return dname


    def mk_filename(file_idx, fname):
        return os.path.join(ensure_dir(file_idx), fname)


    idx = [-1]
    def open_new_output_file(fname):
        try:       
            close(mk_filename(idx[0], fname))
        except Exception:
            pass

        idx[0] += 1
        dst = mk_filename(idx[0], fname)
        print (dst)
        if os.path.exists(dst):
            raise Exception('Cowardly refusing to overwrite %s' % (dst, ))
        return codecs.open(dst, 'w', encoding=args.encoding)


    for fname in os.listdir(args.indir):
        src = os.path.join(args.indir, fname)
        if not os.path.isfile(src):
            raise Exception(
                "Input directory must have only files; found subdirectory '%s'" %
                (src, ))

        n_per_chunk = chunk_size(src, args.encoding)
        idx[0] = -1
        dst = open_new_output_file(fname)
        count = 0
        with codecs.open(src, 'r', encoding=args.encoding) as ifh:
            for line in ifh:
                dst.write(line)

                count += 1
                if count % n_per_chunk == 0:
                    count = 0
                    dst = open_new_output_file(fname)
