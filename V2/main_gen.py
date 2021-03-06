# -*- coding: utf-8 -*-
"""pointer_gen_main.ipynb

Automatically generated by Colaboratory.

"""

import numpy as np
import random
import tensorflow as tf
import tensorflow.nn as nn
import os
import glob

from data_preprocess import Vocab
from data_preprocess import Batcher
from data_preprocess import output_to_words

from model import SummarizationModel

from train_test_eval import get_config
from train_test_eval import run_training
from train_test_eval import restore_model
from train_test_eval import total_num_params

hpm={"hidden_size": 256 , 
     "emb_size": 128,
     "attn_hidden_size":512,
     
     "batch_size":16 , 
     'beam_size':4,
     
     "max_enc_len": 400, 
     'max_dec_len':100, 
     'min_dec_steps':35, 
     'max_dec_steps':100,
     
      
     "pointer_gen":True, 
     "coverage":True,
     "add_coverage":False,
     
     "training":True, 
     'decode':False, 
     'eval' : False,
 
     
     'vocab_size':50000, 
     
     'examples_max_buffer_len' : 40, 
     'batch_max_buffer_len': 10,
     'max_batch_bucket_len':5 ,
     
     'finished':False, 
     'singlepass':False, 
     
     'max_grad_norm':0.8,
     'adagrad_init_acc':0.1, 
     'learning_rate':0.15, 
     'rand_unif_init_mag':0.02, 
     'trunc_norm_init_std':1e-4,
     'cov_loss_weight':1.0,

     'teacher_forcing' : True
     }


vocab_path = "/content/gdrive/My Drive/cnn_stories/vocab"
data_path = "/content/gdrive/My Drive/cnn_stories/train2/*"
checkpoint_dir = "/content/gdrive/My Drive/pointer_gen/checkpoints/"
model_path = "/content/gdrive/My Drive/pointer_gen/checkpoints/model.ckpt-33001"
logdir = "/content/gdrive/My Drive/pointer_gen/logdir"
GAN_gen_checkpoint = "/content/gdrive/My Drive/pointer_gen/GAN_gen_checkpoint/GAN_gen_checkpoint.ckpt"
training_steps = 230000



def build_graph():
  tf.reset_default_graph()
  tf.logging.info('Building the model.')
  if hpm['decode'] :
    hpm['max_dec_len'] = 1
  mod = SummarizationModel(hpm)
  tf.logging.info('Building the graph.')
  mod.add_placeholder()

  device = "/gpu:0" if tf.test.is_gpu_available() else "/cpu:0"
  with tf.device(device):
    mod.build_graph()
  if hpm['training'] or hpm['eval']:
    tf.logging.info('Adding training ops.')
    mod.add_loss()
    mod.add_train_op(device)
  if hpm['decode']:
    assert mod.hpm['batch_size'] == mod.hpm['beam_size']
    mod.add_top_k_likely_outputs()

  if not hpm['teacher_forcing']:
    mod.add_loss()
    #mod.add_top_k_likely_outputs()
    #mod.add_prob_logits_samples()
  return mod



def main():

  mod = build_graph()
  
  if hpm['eval']:
    pass

  if hpm['decode']:
    s = tf.Session(config=get_config())
    init = tf.global_variables_initializer()
    s.run(init)
    restore_model(s, hpm, model_path=model_path, check_path = checkpoint_dir)
    return s, mod
    # and then we can call the beam_decode of the model to decode  th summary (will be implemented later)

  if hpm['training']:
    tf.logging.info('Vocab and Batcher creation')
    vocab = Vocab(vocab_path, hpm['vocab_size'])
    batcher = Batcher(data_path, hpm, vocab)
    tf.logging.info('Starting training.')
    try:
      run_training(mod, batcher, hpm, training_steps, checkpoint_dir, logdir)
    except KeyboardInterrupt:
      tf.logging.info('stop training.')

  if not hpm['teacher_forcing']:
    tf.logging.info('Creating the generator for the GAN')
    with tf.Session(config=get_config()) as s:
      init = tf.global_variables_initializer()
      s.run(init)
      restore_model(s,hpm, model_path=model_path, check_path=checkpoint_dir)
      saver = tf.train.Saver()
      saver_path = saver.save(s, GAN_gen_checkpoint)
      tf.logging.info(saver_path)


if __name__ == '__main__':
  main()

