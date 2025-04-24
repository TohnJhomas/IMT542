import os
from tools import PoetryInterface, WikitionaryInterface
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt 
from matplotlib.gridspec import GridSpec

import numpy as np

def format_poetry_corpus(poetry_corpus):
    """
    Format the poetry corpus for easier access and manipulation.
    """
    poetry_lines = []
    corpus_index = []
    for poem in poetry_corpus:
        title = poem["title"]
        author = poem["author"]
        lines = poem["lines"]
        linecount = poem["linecount"]
        corpus_index.append({
            "title": title,
            "author": author,
            "linecount": linecount
        })
        line_number = 0
        for line in lines:
            # Clean the line by removing leading/trailing whitespace, and replacing hyphens with spaces
            line = line.strip()
            line = line.replace("-", " ")
            line = line.replace("–", " ")
            line = line.replace("—", " ")
            line = line.replace(",", "")
            line = line.replace("!", "")
            line = line.replace("?", "")
            line = line.replace(".", "")

            poetry_lines.append({
                "title": title,
                "author": author,
                "line": line,
                "line_number": line_number
            })
            line_number += 1
    
    # Convert to DataFrame for easier manipulation
    poetry_lines_df = pd.DataFrame(poetry_lines)
    corpus_index_df = pd.DataFrame(corpus_index)
    return poetry_lines_df, corpus_index_df

def count_word_frequencies(poetry_lines_df):
    """
    Count the frequency of each word in the poetry lines.
    """
    word_counter = Counter()
    for line in poetry_lines_df['line']:
        words = line.split()
        word_counter.update(words)
    
    return word_counter

def plot_word_length_vs_frequency(word_counts, lines):
    """
    Creates a scatterplot with word length on the x-axis and word frequency on the y-axis.
    Displays two tables: one with the 10 longest words and one with the 10 most used words.

    Args:
        word_counts (dict): A dictionary where keys are words and values are their frequencies.
    """
    # Prepare data for the scatterplot
    word_lengths = [len(word) for word in word_counts.keys()]
    frequencies = list(word_counts.values())
    words = list(word_counts.keys())

    # Find the 10 longest words
    longest_words = sorted(words, key=len, reverse=True)[:10]
    longest_words_table = [(word, len(word)) for word in longest_words]

    # Find the 10 most used words
    most_used_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    most_used_words_table = [(word, count) for word, count in most_used_words]

    # Create the scatterplot
    fig = plt.figure(figsize=(16, 8))
    gs = fig.add_gridspec(2, 2, width_ratios=[2, 1])

    # Scatterplot
    ax_scatter = fig.add_subplot(gs[:, 0])
    ax_scatter.scatter(word_lengths, frequencies, alpha=0.7, edgecolors='b')
    ax_scatter.set_title("Word Length vs Word Frequency")
    ax_scatter.set_xlabel("Word Length")
    ax_scatter.set_yscale("log")
    ax_scatter.set_ylabel("Word Frequency")
    ax_scatter.grid(True)

    # Table for the 10 longest words
    ax_table1 = fig.add_subplot(gs[0, 1])
    ax_table1.axis("off")
    table1 = ax_table1.table(cellText=[["Word", "Length"]] + longest_words_table, loc="center", cellLoc="center")
    table1.auto_set_font_size(False)
    table1.set_fontsize(10)

    # Table for the 10 most used words
    ax_table2 = fig.add_subplot(gs[1, 1])
    ax_table2.axis("off")
    table2 = ax_table2.table(cellText=[["Word", "Frequency"]] + most_used_words_table, loc="center", cellLoc="center")
    table2.auto_set_font_size(False)
    table2.set_fontsize(10)

    # Adjust layout
    plt.tight_layout()

    

if __name__ == "__main__":
    # Set the author name here
    Poetry_author = "pope"

    poetry_interface = PoetryInterface()
    poetry_corpus = poetry_interface.get_poetry_by_author(Poetry_author)
    if poetry_corpus is None:
        print("No poetry found for the given author.")
        exit(1)
    print(len(poetry_corpus))
    lines, index = format_poetry_corpus(poetry_corpus)
    word_counts = count_word_frequencies(lines)
    plot_word_length_vs_frequency(word_counts,lines)
    plt.show()