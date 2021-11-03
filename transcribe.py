import argparse
from phonemizer import phonemize
from tqdm import tqdm
import pandas as pd


def replace_symbols(symbols):
	symbols_new = symbols.replace('ɐ̃','A').replace('ʊ̃','W').replace('ũ','U').replace('õ','O').replace('ɲ̃','N')
	return symbols_new

def transcribe_sentence(sent):
	phonetic = phonemize(sent,
		language='pt-br',
		backend='espeak',
		preserve_punctuation=True,
		strip=True,
		with_stress=True,
		punctuation_marks=';:,.!?¡¿—…"«»“”.(){}[]')
	return replace_symbols(phonetic)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--file1', required=True, help='original text.txt')
	parser.add_argument('--file2', required=True, help='modified transcription.txt')

	args = parser.parse_args()
	file1 = args.file1
	file2 = args.file2

	phonemes = []
	with open(file1, encoding='utf-8') as f:
		for line in f:
			s = line.strip()
			t = transcribe_sentence(s)
			print(f'{s} --> {t}')
			phonemes.append(t)
	with open(file2, 'w', encoding='utf-8') as f:
		for line in phonemes:
			f.write('%s\n' % line)


if __name__ == "__main__":
	main()
