import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as figure
import matplotlib
from transformers import pipeline, AutoTokenizer, AutoModel
from pylab import rcParams
matplotlib.use("TkAgg")
class Classifier:
    def __init__(self):
        """Downloads, initilizes and loads the zero shot classifier into memory
        """
        self.zero_shot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def classify_text(self, text_to_classify: str, lables:list, multi_label_arg = True):
        """Will take in some text, labels, some flags, it will then produce a zero-shot classification.
        Returns a figure with the probabilities of each possibility. If multi_label_arg
        if False, then the probabilities will be normalized to add up to one

        Args:
            text_to_classify (str): The text you want to classify
            lables (list): A list of strings for all the classes you want to fit into
            multi_label_arg (bool, optional): Weather you allow for more than one class or not. Defaults to True.

        Returns:
            matplotlib.figure: A figure representing the probabilites of the text fitting into each class
        """
        result = self.zero_shot_classifier(
            sequences = text_to_classify,
            candidate_labels = lables,
            multi_label = multi_label_arg
        )
        return self.make_classification_graph(result)


    def make_classification_graph(self, results):
        """Creates the figure from the classification results

        Args:
            results (_type_): The results from a HuggingFace model pipeline

        Returns:
            matplotlib.figure: A figure representing the probabilites of the text fitting into each class
        """
        rcParams['figure.figsize'] = (10, 3)
        plt.clf()
        plt.bar(results["labels"], results["scores"])
        plt.yticks(list(np.arange(0, 1, 0.1)))
        return plt.gcf()





