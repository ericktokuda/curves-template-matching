#!/usr/bin/env python3
"""Utility scripts
"""

import argparse
import time, datetime
import os
from os.path import join as pjoin
import inspect

import sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from myutils import info, create_readme

##########################################################
def get_kernels(kerw, outdir):
    """Geneerate the kernels"""
    info(inspect.stack()[0][3] + '()')
    angles = list(range(0, 180, 30))
    c = int(kerw / 2)
    na = len(angles)
    k = - np.ones((3 * na, kerw, kerw), dtype=int)

    tpl1 = np.zeros((kerw, kerw), dtype=np.uint8) # Corner
    tpl1[c, :] = 1

    tpl2 = np.zeros((kerw, kerw), dtype=np.uint8) # Corner
    tpl2[:c, c] = 1; tpl2[c, :c] = 1

    tpl3 = np.zeros((7, 7), dtype=np.uint8) # Curved line
    for i in range(7):
        for j in range(7):
            if (i-6)**2 + (j-3)**2 >= 6 and (i-6)**2 + (j-3)**2 <= 10:
                tpl3[i, j] = 1
    tpl3[-1, :] = 0

    for i, a in enumerate(angles):
        np.savetxt(pjoin(outdir, 'line_rot{}.txt'.format(a)),
                   np.asarray(Image.fromarray(tpl1).rotate(a)), fmt='%i')
        np.savetxt(pjoin(outdir, 'corner_rot{}.txt'.format(a)),
                   np.asarray(Image.fromarray(tpl2).rotate(a)), fmt='%i')
        np.savetxt(pjoin(outdir, 'curve_rot{}.txt'.format(a)),
                   np.asarray(Image.fromarray(tpl3).rotate(a)), fmt='%i')
    info('Output is in ', outdir)
    info('Adjust each kernel as desired')

##########################################################
def main(outdir):
    """Short description"""
    info(inspect.stack()[0][3] + '()')
    get_kernels(7, '/tmp/out/')

##########################################################
if __name__ == "__main__":
    info(datetime.date.today())
    t0 = time.time()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outdir', default='/tmp/out/', help='Output directory')
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    readmepath = create_readme(sys.argv, args.outdir)

    main(args.outdir)

    info('Elapsed time:{:.02f}s'.format(time.time()-t0))
    info('Output generated in {}'.format(args.outdir))

