import argparse
from phonemizer import phonemize
from tqdm import tqdm
import pandas as pd
import csv


def replace_symbols(symbols):
	symbols_new = symbols.replace('ɐ̃','A').replace('ʊ̃','W').replace('ũ','U').replace('õ','O').replace('ɲ̃','N').replace('ð','T')
	return symbols_new

def transcribe_sentence(sent, lang):
	phonetic = phonemize(sent,
		language=lang,
		backend='espeak',
		preserve_punctuation=True,
		strip=True,
		with_stress=True,
		punctuation_marks=';:,.!?¡¿—…"«»“”.(){}[]')
	return replace_symbols(phonetic)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--lang', default='ptBR', help='language to be used: prBR|enUS (default: ptBR).')
	parser.add_argument('--file1', required=True, help='original train.txt')
	parser.add_argument('--file2', required=True, help='modified train.txt')

	args = parser.parse_args()
	file1 = args.file1
	file2 = args.file2
	accepted_lang = ['ptBR','enUS']
	if args.lang not in accepted_lang:
		raise ValueError(f'Language {args.lang} not supported yet.')
	lang = 'pt-br' if args.lang == 'ptBR'  else 'en-us'
	print(f'\n*LANGUAGE USED: {lang}\n')

	df1 = pd.read_csv(file1, header=None, sep="|", quoting=csv.QUOTE_NONE)
	df2 = df1.copy(deep=True)
	df2.insert(loc=7, column='speaker_id', value=df2[6])
	graphemes = ''
	phonemes = ''
	for i, s in tqdm(enumerate(df2[5]), total=len(df2[5])):
		t = transcribe_sentence(s, lang)
		df2[6][i] = t
		#print(f'{s} --> {t}\n')
#		print('Progress : [ {} / {} ==> {:.5f}% conluded ]'.format(i, len(df2), i/len(df2)*100), end='\r')
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
