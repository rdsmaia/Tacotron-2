# Tacotron code for multilingual ptBR training

Tacotron repo to train a multispeaker ptBR TTS.

This repo is a fork of Rayhane Mama's Tacotron-2 repo. The main modifications are:
* multilingual TTS
* no WaveNet
* changes in the speech processing set-up
* support for external speaker embeddings
* support to add speaker embeddings at different locations: encoder's output, prenet output and postnet
* changes in text processing and symbols for phonetic inputs in ptBR.
