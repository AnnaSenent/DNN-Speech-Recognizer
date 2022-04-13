# DNN-Speech-Recognizer

### Introduction

This is thethird project in [Udacity](udacity.com)'s [Natural Language Processing Nanodegree](https://www.udacity.com/course/natural-language-processing-nanodegree--nd892). It has as its aim to build a deep neural network that functions as part of an end-to-end automatic speech recognition (ASR) pipeline. When completed the pipeline will take raw audio as input and return a predicted transcription of the spoken language.

The [LibriSpeech dataset](http://www.openslr.org/12/) is used to train and evaluate the models.

In this notebook, I will cover all the steps that are needed to complete this project.

### Setup

GPU acceleration is required in order for the project to run efficiently. I worked on Udacity workspaces, which provide GPU support by conveniently switching to GPU mode.


### Required libraries

- Numpy
- Matplotlib
- Keras
- Tensorflow
- python_speech_features
- Librosa
