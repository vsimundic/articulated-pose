# python evaluation/compute_gt_pose.py --item='eyeglasses' --domain='unseen' --nocs='NPCS' --save


# python evaluation/baseline_naocs.py --item='eyeglasses' --domain='unseen' --nocs='ANCSH'
# python evaluation/baseline_npcs.py --item='eyeglasses' --domain='unseen' --nocs='NPCS'

# # run our processing over test group
# python evaluation/pose_multi_process.py --item='eyeglasses' --domain='unseen'

# pose & relative joint rotation
# python evaluation/eval_pose_err.py --item='eyeglasses' --domain='unseen' --nocs='NPCS'

# # 3d miou estimation
# python evaluation/compute_miou.py --item='eyeglasses' --domain='unseen' --nocs='ANCSH'

# # performance on joint estimations 
python evaluation/eval_joint_params.py --item='eyeglasses' --domain='unseen' --nocs='ANCSH'