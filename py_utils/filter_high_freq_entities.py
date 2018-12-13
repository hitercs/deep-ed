import argparse

def do_filtering(in_fn, out_fn, topN=200000):
    with open(in_fn, encoding="utf-8", mode="r", buffering=100000) as in_fp:
        with open(out_fn, encoding="utf-8", mode="w", buffering=100000) as out_fp:
            for line_id, line in enumerate(in_fp):
                if line_id >= topN:
                    break
                words = line.strip().split("\t")
                out_fp.write("{}\t{}\n".format(words[1], words[0]))
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-in-fn", "--in-fn", type=str, default="")
    parser.add_argument("-out-fn", "--out-fn", type=str, default="")
    parser.add_argument("-topN", "--topN", type=int, default=200000)
    args = parser.parse_args()
    do_filtering(args.in_fn, args.out_fn, args.topN)