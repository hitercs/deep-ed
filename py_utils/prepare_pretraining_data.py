#encoding: utf-8
import codecs
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize

def process_one_line(line):
    fields = line.strip().split("\t")
    # fields[3] is the left context
    # fields[4] is the right context
    try:
        left_ctx = fields[3]
        right_ctx = fields[4]
        left_ctx_sents = sent_tokenize(left_ctx)
        right_ctx_sents = sent_tokenize(right_ctx)
        left_ctx_sents_tokenize = []
        right_ctx_sents_tokenize = []
        for s in left_ctx_sents:
            left_ctx_sents_tokenize.append(" ".join(word_tokenize(s.strip())))
        for s in right_ctx_sents:
            right_ctx_sents_tokenize.append(" ".join(word_tokenize(s.strip())))

        # update fields with new ctx
        fields[3] = "###".join(left_ctx_sents_tokenize)
        fields[4] = "###".join(right_ctx_sents_tokenize)
    except IndexError:
        print(line)
        return ""
    return "\t".join(fields)


def run(in_fn, out_fn, error_fn):
    with codecs.open(in_fn, encoding="utf-8", mode="r", buffering=10000) as in_fp:
        with codecs.open(out_fn, encoding="utf-8", mode="w", buffering=10000) as out_fp:
            with codecs.open(error_fn, encoding="utf-8", mode="w", buffering=10000) as error_fp:            
                num = 0
                for line in in_fp:
                    num += 1
                    if num % 100000 == 0:
                        print("processing {}".format(num))
                    re_line = process_one_line(line)
                    if re_line.strip() != "":
                        out_fp.write("{}\n".format(re_line))
                    else:
                        error_fp.write("{}\n".format(line))
print(process_one_line("""12	Anarchism	political philosophy	Anarchism Anarchism is a	that advocates stateless societies often defined as self-governed voluntary institutions, but that several authors have defined as more specific institutions based on non- hierarchical free associations . Anarchism holds the state to be undesirable, unnecessary, or harmful. While anti-statism is central, some argue that anarchism entails opposing authority or hierarchical organization in the conduct of human relations, including, but not limited to, the state system. As a subtle and anti-dogmatic philosophy, anarchism draws on many currents of thought and strategy. Anarchism does not offer a fixed body of doctrine from a single particular world view, instead fluxing and flowing as	CANDIDATES	23040,0.989,Political philosophy	3225498,0.007,Libertarianism	410138,0.002,Marilyn Musgrave	39704,0.001,Social contract	19280734,0.000,Liberalism	24388,0.000,Political science	1508860,0.000,Third International Theory	GT:	1,23040,0.989,Political philosophy"""))
run(r"/home/v-shuach/Workspace/deep-ed/data/generated/wiki_hyperlink_contexts_keep_punc.csv",
    r"/home/v-shuach/Workspace/deep-ed/data/generated/wiki_hyperlink_contexts_keep_punc_tokenize2.csv",
    r"/home/v-shuach/Workspace/deep-ed/data/generated/tok_error_parse.csv")