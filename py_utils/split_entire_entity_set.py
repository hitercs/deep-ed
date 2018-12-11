import argparse
import os
import math

parser = argparse.ArgumentParser()
parser.add_argument("-in-fn", "--in-fn", type=str, default="")
parser.add_argument("-out-dir", "--out-dir", type=str, default="")
parser.add_argument("-file-num", "--file-num", type=int, default=1000000)
args = parser.parse_args()

def split_big_file(in_fn, out_dir, file_num):
    with open(in_fn, encoding="utf-8", mode="r", buffering=100000) as in_fp:
        all_lines = in_fp.readlines()
        total_lines = len(all_lines)
        print(total_lines)
        parts = math.ceil(total_lines / file_num)
        for i in range(parts):
            with open(os.path.join(out_dir, "wiki_name_id_map_part{}.txt".format(i+1)), encoding="utf-8", mode="w") as out_fp:
                out_fp.writelines(all_lines[i*file_num:(i+1)*file_num])
                
split_big_file(args.in_fn, args.out_dir, args.file_num)