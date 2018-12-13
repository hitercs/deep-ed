import argparse
from tensorboardX import SummaryWriter
import os
import random
random.seed(12345)

class Util:
    @staticmethod
    def add_vocab(vocab, key):
        if key not in vocab:
            vocab[key] = 1
        else:
            vocab[key] += 1


def load_entity_set(entity_fn):
    entity_set = set()
    with open(entity_fn, encoding="utf-8", mode="r", buffering=100000) as fp:
        for line in fp:
            words = line.strip().split("\t")
            entity_set.add(words[0])
    return entity_set


def do_filtering(anchor_fn, entity_set, writer, re_anchor_fn, keep_topN=100):
    anchor_dict = dict()
    linked_freq = dict()
    freq_dist_num = dict()
    num = 0
    with open(anchor_fn, encoding="utf-8", mode="r", buffering=100000) as anchor_fp:
        for line in anchor_fp:
            words = line.strip().split("\t")
            gold_ans = words[-1].split(",")[-1]
            num += 1
            if num % 1000000 == 0:
                print("processing {} lines...".format(num))
                
            if gold_ans in entity_set:
                if gold_ans not in anchor_dict:
                    anchor_dict[gold_ans] = [line]
                    linked_freq[gold_ans] = 1
                else:
                    anchor_dict[gold_ans].append(line)
                    linked_freq[gold_ans] += 1
        for gold_ans in linked_freq:
            Util.add_vocab(freq_dist_num, linked_freq[gold_ans])
        sorted_freq_dist_num = sorted(freq_dist_num.items(), key=lambda x:x[0])
        acc = 0
        total = len(linked_freq)
        print("total golden ids = ", total)
        for x in sorted_freq_dist_num:
            acc += x[1]
            writer.add_scalar("data-statistics/entity_anchor_freq_dist", acc/float(total), x[0])
        print("acc is ", acc)
        writer.close()
        total_anchor_num = 0
        with open(re_anchor_fn, encoding="utf-8", mode="w", buffering=100000) as re_anchor_fp:
            for gold_ans in anchor_dict:
                random.shuffle(anchor_dict[gold_ans])
                total_anchor_num += len(anchor_dict[gold_ans][0:keep_topN])
                re_anchor_fp.writelines(anchor_dict[gold_ans][0:keep_topN])
        print("total anchor num is ", total_anchor_num)

if __name__  == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-entity-fn", "--entity-fn", type=str, default="/home/v-shuach/Workspace/deep-ed/data/basic_data/partition/wiki_name_id_map_part6.txt")
    parser.add_argument("-anchor-fn", "--anchor-fn", type=str, default="/home/v-shuach/Workspace/deep-ed/data/generated/wiki_hyperlink_contexts_keep_punc_tokenize_clean.csv")
    parser.add_argument("-re-anchor-fn", "--re-anchor-fn", type=str, default="/home/v-shuach/Workspace/deep-ed/data/generated/anchor_filtered/high_freq_20W_ent.csv")
    parser.add_argument("-log-dir", "--log-dir", type=str, default="/home/v-shuach/Workspace/deep-ed/data/tensorboard_log/")
    parser.add_argument("-topN", "--topN", type=int, default=100)
    parser.add_argument("-log-name", "--log-name", type=str, default="")
    args = parser.parse_args()
    writer = SummaryWriter(os.path.join(args.log_dir, args.log_name))
    print("loadding entity set")
    entity_set = load_entity_set(args.entity_fn)
    print("loadding {} entities".format(len(entity_set)))
    do_filtering(args.anchor_fn, entity_set, writer, args.re_anchor_fn, args.topN)