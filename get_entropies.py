#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import matplotlib.pyplot as plt

# Function to parse the dp.ps file and return the square roots of the probabilities
def parse_dp_ps(file_path):
    probabilities = {}
    with open(file_path, 'r') as file:
        for line in file:
            if 'ubox' in line:
                parts = line.split()
                if len(parts) == 4:
                    i, j, sqrt_p = int(parts[0]), int(parts[1]), float(parts[2])
                    probabilities[(i, j)] = sqrt_p ** 2  # Square the value to get the actual probability
    return probabilities

window_size = 1


def calculate_local_entropy(probabilities, start, end):
    # Calculate the local entropy for a window of the sequence
    local_entropy = -np.sum([p * np.log10(p) for (_, _), p in probabilities.items() if start <= _ <= end])
    return local_entropy

def calculate_smoothed_entropies(probabilities, sequence_length, window_size):
    # Ensure window_size is odd for a centered window
    if window_size % 2 == 0:
        window_size += 1

    # Calculate local entropies using a sliding window
    half_window = window_size // 2
    smoothed_entropies = []
    for i in range(1, sequence_length + 1):
        start = max(i - half_window, 1)
        end = min(i + half_window, sequence_length)
        local_entropies = [calculate_local_entropy(probabilities, j, j) for j in range(start, end + 1)]
        median_entropy = np.median(local_entropies)
        smoothed_entropies.append(median_entropy)
    
    return np.array(smoothed_entropies)



def calculate_entropies(probabilities, sequence_length):
    entropies = np.zeros(sequence_length)
    # Calculate the total entropy
    total_entropy = -np.sum([p * np.log10(p) for (_, _), p in probabilities.items()])
    # Normalize by the sequence length to get the average entropy per base
    average_entropy = total_entropy / sequence_length
    
    # Assuming you want to set this average entropy for each base position
    entropies.fill(average_entropy)
    return entropies


# Function to calculate the entropy for each base position including unpaired probabilities
# RNAfold webserver style
def _calculate_entropies(probabilities, sequence_length):
    entropies = np.zeros(sequence_length)
    for i in range(1, sequence_length + 1):
        p_i = [prob for (base_i, base_j), prob in probabilities.items() if base_i == i or base_j == i]
        q_i = 1 - sum(p_i)
        entropy_i = -sum(p * np.log(p) for p in p_i if p > 0)  # Sum of -p_ij * log(p_ij)
        entropy_i -= q_i * np.log(q_i) if q_i > 0 else 0  # Subtract -q_i * log(q_i)
        entropies[i-1] = entropy_i
    return entropies



# Function to calculate the entropy for each base position
# Most basic style
def _calculate_entropies(probabilities, sequence_length):
    entropies = np.zeros(sequence_length)
    for (i, j), p in probabilities.items():
#        entropies[i-1] += p * np.log(p) if p > 0 else 0
#        entropies[j-1] += p * np.log(p) if p > 0 else 0
        entropies[i-1] += p * np.log2(p) if p > 0 else 0
        entropies[j-1] += p * np.log2(p) if p > 0 else 0


    return -entropies






# Function to plot the entropies with a filled style
def _plot_entropies(entropies):
    plt.figure(figsize=(10, 5))
    plt.fill_between(range(1, len(entropies) + 1), entropies, color='brown', step='mid', alpha=0.5)
    plt.title('Entropy Plot')
    plt.xlabel('Base Position')
    plt.ylabel('Entropy')
    plt.ylim(0, max(entropies) * 1.1)  # Set y-axis limit to give some space above the highest peak
    plt.grid(True)  # Optional: Adds a grid to the plot
    plt.gca().set_facecolor('white')  # Set background to white
    plt.show()




# Function to plot the entropies with a filled area under the curve, no outline, no grid, and save as PNG
def plot_entropies(entropies, filename):
    plt.figure(figsize=(10, 5))
    # Fill the area under the curve
#    plt.fill_between(range(1, len(entropies) + 1), entropies, color='brown', alpha=0.5, edgecolor='none')
    plt.fill_between(range(1, len(entropies) + 1), entropies, color='brown', alpha=0.5, edgecolor='none', linewidth=0)


    # Set plot title and labels
    plt.title('Entropy Plot')
    plt.xlabel('Base Position')
    plt.ylabel('Entropy')
    # Set y-axis limit to give some space above the highest peak
    plt.ylim(0, max(entropies) * 1.1)
    # Set background to white
    plt.gca().set_facecolor('white')
    # Save the figure as a PNG file with 300 dpi
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()


# Function to plot the entropies
def _plot_entropies(entropies):
    plt.figure(figsize=(10, 5))
    plt.plot(entropies, marker='o')
    plt.title('Entropy Plot')
    plt.xlabel('Base Position')
    plt.ylabel('Entropy')
    plt.show()

# Function to read the sequence length from a .fas file
def get_sequence_length(fas_file_path):
    with open(fas_file_path, 'r') as file:
        # Skip the first line which is the header
        file.readline()
        # The second line is the sequence
        sequence = file.readline().strip()
        return len(sequence)

# Main script execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate and plot entropies from a dp.ps file.")
    parser.add_argument('ps_file', type=str, help='Path to the dp.ps file containing the base pairing probabilities.')
    parser.add_argument('fas_file', type=str, help='Path to the .fas file to determine the sequence length.')

    args = parser.parse_args()

    sequence_length = get_sequence_length(args.fas_file)
    probabilities = parse_dp_ps(args.ps_file)
    entropies = calculate_entropies(probabilities, sequence_length)
    plot_entropies(entropies, 'entropy_plot.png')
    smoothed_entropies = calculate_smoothed_entropies(probabilities, sequence_length, window_size)
    plot_entropies(smoothed_entropies, 'entropy_smoothed_plot.png')