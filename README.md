# Tacotron code for multispeaker ptBR TTS

Tacotron repo to train a multispeaker ptBR TTS.

This repo is a fork of Rayhane Mama's Tacotron-2 repo (https://github.com/Rayhane-mamah/Tacotron-2). The modifications are:
* multilingual TTS;
* no WaveNet;
* changes in the speech processing set-up;
* support for external speaker embeddings;
* support to add speaker embeddings at different locations: encoder's output, prenet output and postnet;
* changes in text processing and symbols for phonetic inputs in ptBR.

# Set-up

```shell
pip install -r requirements.txt
```

# Data preparation and preprocessing

* Download the data from https://www.kaggle.com/datasets/mediatechlab/gneutralspeech and:

- Downsample the waveforms from 44.1kHz to 22.05kHz.
- Create a metadata file containing filename, normalized text and speaker ids.

```shell
unzip archive.zip
mkdir -p smt_propor2020/wavs
for f in voz_base_44kHz_16bit/wavs/*.wav; do sox $f -r 22050 -c 1 smt_propor2020/wavs/$(basename $f) rate -h; done
awk -F "|" '{OFS="|",print $1,$3"|78"}' voz_base_44kHz_16bit/metadata_voz_base_norm.csv > smt_propor2020/metadata.csv
```

* Extract mel spectrograms.
```shell
python preprocess.py --dataset smt_propor2020
```

* Run grapheme-phoneme conversion
```shell
python transcribe_metadata.py --file1 training_data/train.txt --file2 training_data/train_transcribed.txt
```

# Training

* Train the model.
```shell
python train.py --name v001 --tacotron_training training_data/train_transcribed.txt
```

# Synthesis

* Transcribe your text (run g2p)
```shell
python transcribe.py --file1 test_sentences_ptBR.txt --file2 test_sentences_ptBR_transcriptions.txt
```

* Run the synthesizer (phonemes -> mel spectrograms)
```shell
python synthesize.py --name v001 --text_list test_sentences_ptBR_transcriptions.txt --speaker_id 78
```

* Synthesize speech using a pre-trained HiFi-GAN model (coming soon...)

# Credits

* Rayhane Mamma's Tacotron: https://github.com/Rayhane-mamah/Tacotron-2
* Jungil Kong's HiFi-GAN: https://github.com/jik876/hifi-gan
* Phonemizer: https://github.com/bootphon/phonemizer
