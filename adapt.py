import argparse, os, infolog
from time import sleep

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from hparams_adapt import hparams
from infolog import log
from tacotron.adapt import tacotron_adapt

log = infolog.log

def prepare_run(args):
	modified_hp = hparams.parse(args.hparams)
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(args.tf_log_level)
	run_name = args.name
	log_dir = os.path.join(args.base_dir, 'logs-{}'.format(run_name))
	os.makedirs(log_dir, exist_ok=True)
	infolog.init(os.path.join(log_dir, 'Terminal_train_log'), run_name, args.slack_url)
	base_model_dir = os.path.join(args.base_model, 'taco_pretrained')
	return log_dir, base_model_dir, modified_hp

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--base_dir', default='')
	parser.add_argument('--hparams', default='',
		help='Hyperparameter overrides as a comma-separated list of name=value pairs')
	parser.add_argument('--tacotron_input', default='training_data/train.txt')
	parser.add_argument('--name',
		help='Name of logging directory.')
	parser.add_argument('--summary_interval', type=int, default=1,
		help='Steps between running summary ops')
	parser.add_argument('--checkpoint_interval', type=int, default=1,
		help='Steps between writing checkpoints')
	parser.add_argument('--tacotron_train_steps', type=int, default=200001,
		help='total number of tacotron training steps')
	parser.add_argument('--tf_log_level', type=int, default=1,
		help='Tensorflow C++ log level.')
	parser.add_argument('--slack_url', default=None,
		help='slack webhook notification destination link')
	parser.add_argument('--base_model', default='logs-Tacotron',
		help='path to the log dir of the base model (default=logs-Tacotron).')
	args = parser.parse_args()

	log_dir, base_model_dir, hparams = prepare_run(args)
	tacotron_adapt(args, log_dir, base_model_dir, hparams)

if __name__ == '__main__':
	main()
