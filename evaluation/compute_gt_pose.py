from h5py._hl import base
import numpy as np
import os
import sys
import time

from numpy.lib.npyio import save
import h5py
import pickle
import argparse

import _init_paths
from lib.data_utils import get_demo_h5, get_full_test
from lib.aligning import estimateSimilarityUmeyama
from global_info import global_info

def compose_rt(rotation, translation):
    aligned_RT = np.zeros((4, 4), dtype=np.float32)
    aligned_RT[:3, :3] = rotation.transpose()
    aligned_RT[:3, 3]  = translation
    aligned_RT[3, 3]   = 1
    return aligned_RT

if __name__ == '__main__':
    infos     = global_info()
    my_dir    = infos.base_path
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', default='unseen', help='which sub test set to choose')
    parser.add_argument('--nocs', default='ANCSH', help='which nocs type to use')
    parser.add_argument('--item', default='drawer', help='object category for benchmarking')
    parser.add_argument('--save', action='store_true', help='save err to pickles')

    args = parser.parse_args()

    base_path       = my_dir + '/results'

    infos           = global_info()
    dset_info       = infos.datasets[args.item]
    num_parts       = dset_info.num_parts
    num_ins         = dset_info.num_object
    unseen_instances= dset_info.test_list
    special_ins     = dset_info.spec_list
    main_exp        = dset_info.exp
    baseline_exp    = dset_info.baseline
    test_h5_path    = base_path + '/test_pred/{}'.format(main_exp)
    all_test_h5     = os.listdir(test_h5_path)
    # print("[DEBUG]", all_test_h5)
    test_group      = get_full_test(all_test_h5, unseen_instances, domain=args.domain, spec_instances=special_ins)
    print('we have {} testing data for {} {}'.format(len(test_group), args.domain, args.item))

    all_rts = {}
    file_name = base_path + '/pickle/{}/{}_{}_{}_rt.pkl'.format(main_exp, args.domain, args.nocs, args.item)
    save_path = base_path + '/pickle/{}/'.format(main_exp)

    file_bad_path = test_h5_path + '/bad.txt'
    fbad = open(file_bad_path, 'w')

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    problem_ins = []
    start_time = time.time()
    for i in range(len(test_group)):
        # try:
        h5_file    =  test_h5_path + '/' + test_group[i]
        # print('Now checking {}: {}'.format(i, h5_file))
        # if test_group[i] == '45841_9_15.h5':
        #     print("ayy rip")

        if test_group[i].split('_')[0] in problem_ins:
            print('skipping {}: {}'.format(i, h5_file))
            fbad.write('{}\n'.format(test_group[i]))
            continue
        hf         =  h5py.File(h5_file, 'r')
        basename   =  hf.attrs['basename']

        nocs_gt        =  {}
        nocs_gt['pn']  =  hf['nocs_gt'][()]
        if args.nocs == 'NPCS':
            nocs_gt['gn']  =  hf['nocs_gt_g'][()]
        input_pts      =  hf['P'][()]
        mask_gt        =  hf['cls_gt'][()]
        name_info      = basename.split('_')
        instance       = name_info[0]
        art_index      = name_info[1]
        frame_order    = name_info[2]

        part_idx_list_gt   = []
        part_idx_list_pred   = []
        rt_gt    = []
        scale_gt = []

        flag_skipping = False
        for j in range(num_parts):
            part_idx_list_gt.append(np.where(mask_gt==j)[0])

            if len(part_idx_list_gt[j]) == 0:
                flag_skipping = True
                break

            if args.nocs == 'ANCSH':
                a = nocs_gt['pn'][part_idx_list_gt[j], :]
            else:
                a = nocs_gt['gn'][part_idx_list_gt[j], :]
            c = input_pts[part_idx_list_gt[j], :]
            s, r, t, rt = estimateSimilarityUmeyama(a.transpose(), c.transpose())
            rt_gt.append(compose_rt(r, t))
            scale_gt.append(s)

        if flag_skipping:
            # print("skipping {}".format(i))
            print('skipping {}: {}'.format(i, h5_file))

            fbad.write('{}\n'.format(test_group[i]))
            continue
        
        rts_dict   = {}
        scale_dict = {}
        rt_dict    = {}
        rt_dict['gt']    = rt_gt
        scale_dict['gt'] = scale_gt
        rts_dict['scale']  = scale_dict
        rts_dict['rt']     = rt_dict
        all_rts[basename.split('.')[0]]  = rts_dict
        # except Exception as e:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno)
     
    fbad.close()

    if args.save or True:
        with open(file_name, 'wb') as f:
            pickle.dump(all_rts, f, protocol=2)
            # print(all_rts)
            print('saving to ', file_name)
    print('takes {} seconds', time.time() - start_time)
