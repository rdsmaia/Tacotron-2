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
	parser.add_argument('--file1', required=True, help='original train.txt')
	parser.add_argument('--file2', required=True, help='modified train.txt')

	args = parser.parse_args()
	file1 = args.file1
	file2 = args.file2

	df1=pd.read_csv(file1, header=None, sep="|")
	df2 = df1.copy(deep=True)
	graphemes = ''
	phonemes = ''
	for i, s in enumerate(df2[5]):
		t = transcribe_sentence(s)
		df2[6][i] = t
#		print(f'{s} --> {t}\n')
		print('Progress : [ {} / {} ==> {:.5f}% conluded ]'.format(i, len(df2), i/len(df2)*100), end='\r')
		graphemes += s
		phonemes += t
	df2.to_csv(file2, sep="|", header=None, index=False)

	grapheme_set = set(list(graphemes))
	phoneme_set = set(list(phonemes))
	grapheme_symbols = ''.join(list(grapheme_set))
	phoneme_symbols = ''.join(list(phoneme_set))

	print(f'\n\nGRAPHEME SET:\n {grapheme_set}')
	print(f'PHONEME SET:\n {phoneme_set}')
	print(f'GRAPHEME SYMBOLS:\n {grapheme_symbols}')
	print(f'PHONEME SYMBOLS:\n {phoneme_symbols}\n\n')


if __name__ == "__main__":
	main()
