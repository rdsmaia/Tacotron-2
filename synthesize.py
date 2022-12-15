import argparse
import os
from warnings import warn
from time import sleep

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from hparams import hparams
from infolog import log
from tacotron.synthesize import tacotron_synthesize


def prepare_run(args):
	modified_hp = hparams.parse(args.hparams)
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

	run_name = args.name
	taco_checkpoint = os.path.join('logs-' + run_name, 'taco_' + args.checkpoint)

	return taco_checkpoint, modified_hp

def get_sentences(args):
	if args.text_list != '':
		with open(args.text_list, 'rb') as f:
			sentences = list(map(lambda l: l.decode("utf-8")[:-1], f.readlines()))
	else:
		sentences = hparams.sentences
	return sentences

def main():
	accepted_models = ['Tacotron']
	accepted_modes = ['eval', 'synthesis', 'live']
	parser = argparse.ArgumentParser()
	parser.add_argument('--checkpoint', default='pretrained/', help='Path to model checkpoint')
	parser.add_argument('--hparams', default='',
		help='Hyperparameter overrides as a comma-separated list of name=value pairs')
	parser.add_argument('--name', help='Name of logging directory of Tacotron.')
	parser.add_argument('--input_dir', default='training_data/', help='folder to contain inputs sentences/targets.')
	parser.add_argument('--output_dir', default='output/', help='folder to contain synthesized mel spectrograms')
	parser.add_argument('--mode', default='eval', help='mode of run: can be one of {}'.format(accepted_modes))
	parser.add_argument('--model', default='Tacotron', help='at the moment we only have Tacotron.')
	parser.add_argument('--GTA', type=bool, default=True, help='Ground truth aligned synthesis, defaults to True, only considered in synthesis mode')
	parser.add_argument('--text_list', default='', help='Text file contains list of texts to be synthesized. Valid if mode=eval')
	parser.add_argument('--speaker_id', default=0, help='Defines the speakers id to use at synthesis (default=0).')
	args = parser.parse_args()

	if args.model not in accepted_models:
		raise ValueError('accepted models are: {}, found {}'.format(accepted_models, args.model))

	if args.mode not in accepted_modes:
		raise ValueError('accepted modes are: {}, found {}'.format(accepted_modes, args.mode))

	if args.GTA not in (True, False):
		raise ValueError('GTA option must be either True or False')

	taco_checkpoint, hparams = prepare_run(args)
	sentences = get_sentences(args)

	_ = tacotron_synthesize(args, hparams, taco_checkpoint, sentences)


if __name__ == '__main__':
	main()
