import os
import time
import pickle
import argparse
import numpy as np

# custom packages
import _init_paths
from global_info import global_info
from evaluation.parallel_ancsh_pose import solver_ransac_nonlinear
from lib.data_utils import get_test_group

infos           = global_info()
print(infos.datasets['eyeglasses'])

# run non-linear optimization over predictions from PNOCS and joints params
parser = argparse.ArgumentParser()
parser.add_argument('--domain', default='unseen', help='which sub test set to choose')
parser.add_argument('--nocs', default='part', help='which sub test set to choose')
parser.add_argument('--item', default='eyeglasses', help='object category for benchmarking')
parser.add_argument('-f', default='default', help='default string for jupyter')

args = parser.parse_args()

dset_info       = infos.datasets[args.item]
num_parts       = dset_info.num_parts
num_ins         = dset_info.num_object
unseen_instances= dset_info.test_list
special_ins     = dset_info.spec_list
main_exp        = dset_info.exp
baseline_exp    = dset_info.baseline
test_exp        = main_exp
my_dir          = infos.base_path
base_path       = my_dir + '/results/test_pred'
choose_threshold = 0.1

# testing
test_h5_path    = base_path + '/{}'.format(test_exp)
all_test_h5     = os.listdir(test_h5_path)
test_group      = get_test_group(all_test_h5, unseen_instances, domain=args.domain, spec_instances=special_ins)

problem_ins     = []
print('we have {} testing data for {} {}'.format(len(test_group), args.domain, args.item))

start_time = time.time()
rts_all = pickle.load( open(my_dir + '/results/pickle/{}/{}_{}_{}_rt.pkl'.format(main_exp, args.domain, args.nocs, args.item), 'rb' ))

directory = my_dir + '/results/pickle/{}'.format(main_exp)
file_name = directory + '/{}_{}_{}_{}_rt_ours_{}.pkl'.format(baseline_exp, args.domain, args.nocs, args.item, choose_threshold)

s_ind = 0
e_ind = 10
solver_ransac_nonlinear(s_ind, e_ind, test_exp, baseline_exp, choose_threshold, num_parts, test_group, problem_ins, rts_all, file_name)
