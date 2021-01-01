#! /usr/bin/env python
# -*- coding:utf-8 -*-
#=====================================
# Author      : Zhaoyoubiao
# File name   : lstm_crf_predict.py
# Create date : 2020/12/31 17:07
# IDE         : pycharm
#=====================================
import tensorflow as tf
import os

from model_lstm_crf import MyModel
from utils import DataProcessor_LSTM as DataProcessor
from utils import load_vocabulary
from utils import extract_kvpairs_in_bio
from utils import cal_f1_score

os.environ['CUDA_VISIBLE_DEVICES'] = '3'
lstm_crf_ckpt = "models/"
base_dir = "./data/ner_data"
w2i_char, i2w_char = load_vocabulary(os.path.join(base_dir, "vocab.txt"))
w2i_bio, i2w_bio = load_vocabulary(os.path.join(base_dir, "vocab_bio.txt"))


data_processor = DataProcessor(
    os.path.join(base_dir, 'valid.txt'),
    os.path.join(base_dir, "valid_bio.txt"),
    w2i_char,
    w2i_bio,
    shuffling=True
)

model = MyModel(embedding_dim=300,
                hidden_dim=300,
                vocab_size_char=len(w2i_char),
                vocab_size_bio=len(w2i_bio),
                use_crf=True)

tf_config = tf.ConfigProto(allow_soft_placement=True)
tf_config.gpu_options.allow_growth = True
ckpt = tf.train.get_checkpoint_state(lstm_crf_ckpt)
with tf.Session(config=tf_config) as sess:
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver(max_to_keep=50)
    saver.restore(sess, ckpt.model_checkpoint_path)
    # tf.train.latest_checkpoint(lstm_crf_ckpt)
    batch_size = 32

    preds_kvpair = []
    golds_kvpair = []
    while True:
        (inputs_seq_batch,
         inputs_seq_len_batch,
         outputs_seq_batch) = data_processor.get_batch(batch_size)

        feed_dict = {
            model.inputs_seq: inputs_seq_batch,
            model.inputs_seq_len: inputs_seq_len_batch,
            model.outputs_seq: outputs_seq_batch
        }

        preds_seq_batch = sess.run(model.outputs, feed_dict)

        for pred_seq, gold_seq, input_seq, l in zip(preds_seq_batch,
                                                    outputs_seq_batch,
                                                    inputs_seq_batch,
                                                    inputs_seq_len_batch):
            pred_seq = [i2w_bio[i] for i in pred_seq[:l]]
            gold_seq = [i2w_bio[i] for i in gold_seq[:l]]
            char_seq = [i2w_char[i] for i in input_seq[:l]]
            pred_kvpair = extract_kvpairs_in_bio(pred_seq, char_seq)
            gold_kvpair = extract_kvpairs_in_bio(gold_seq, char_seq)

            preds_kvpair.append(pred_kvpair)
            golds_kvpair.append(gold_kvpair)

