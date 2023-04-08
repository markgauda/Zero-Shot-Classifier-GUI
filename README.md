# Zero-Shot-Classifier-GUI
This is a GUI wrapper for the HuggingFace Pipeline for zero shot classifiers

## Overview
This project was designed as a way for me to practice GUI developement, and AI pipelining. This uses the facebook/bart-large-mnli model from huging face as a zeroshot classifier (found in the classifier_class module). The GUI.py file defines the logic to create a graphical user interface for the bart-large-mnli model as a zeroshot classifier. The GUI makes this tech much more accessable to people of all techonological levels.

Overall this project was great practice, and a fun weekend project to teach myself how to use hugging face models programatically, and how to develope simple GUI applications. I recognize that the steps involved to install this application work against the idea of using a GUI to simplify things. I am working on making an executable release for this, so it can be insatlled and run without much effort.

## Instalation
I recomend initilizing a virtual environment for instling this project

In addition to the requierments.txt, you are going to need:
- [The latest CUDA Toolkit drivers](https://developer.nvidia.com/cuda-11-7-0-download-archive)
- [PyToarch](https://pytorch.org/)

After you have installed these things, you can `pip install -r requierments.txt`

This should be enough to get the project working. If you are running from a virtual environment, make sure you start GUI.py from an activated terminal.

## Screenshots
