# Tacotron code for multilingual ptBR training

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

# Data preprocessing

```shell
python preprocess.py --dataset smt_propor202
```

```shell
python transcribe_metadata.py --file1 training_data/train.txt --file2 training_data/train_transcribed.txt
```

# Training

```shell
python train.py --name v001 --tacotron_training training_data/train_transcribed.txt
```


