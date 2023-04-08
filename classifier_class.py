import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as figure
import matplotlib
from transformers import pipeline, AutoTokenizer, AutoModel
from pylab import rcParams
matplotlib.use("TkAgg")
class Classifier:
    def __init__(self):
        self.zero_shot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def classify_text(self, text_to_classify: str, lables:list, multi_label_arg = True):
        result = self.zero_shot_classifier(
            sequences = text_to_classify,
            candidate_labels = lables,
            multi_label = multi_label_arg
        )
        return self.make_classification_graph(result)


    def make_classification_graph(self, results):

        rcParams['figure.figsize'] = (10, 3)
        plt.clf()
        plt.bar(results["labels"], results["scores"])
        plt.yticks(list(np.arange(0, 1, 0.1)))
        return plt.gcf()





