import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import zscore
import seaborn as sns
import matplotlib.pyplot as plt


discovery_algorithms = ["IM", "HM", "IMF"]
# conformance_algorithms = ["token", "alignments"]
conformance_algorithms = ["token"]

fitness_results = {}


def get_fitness_results():
    # Iterate through each discovery algorithm
    for discovery_alg in discovery_algorithms:
        # Read the CSV file for the current discovery algorithm
        file_path = f"2. Iteration/Results/output_{discovery_alg}_token.csv"

        df = pd.read_csv(file_path, index_col=0, decimal=',')  

        # Convert values to numeric
        df = df.apply(lambda x: pd.to_numeric(x.str.replace(',', '.'), errors='coerce'))

        # Calculate mean and standard deviation for each model
        # mean_values = df.mean()
        # std_values = df.std()

        # Store the raw fitness values in the dictionary
        fitness_results[discovery_alg] = df

    return fitness_results


# Correlation Analysis
def cor_analysis(fitness_results):
    fitness_values_df = pd.concat(fitness_results.values(), axis=1, keys=fitness_results.keys())
    correlation_matrix = fitness_values_df.corr()

    print("Correlation Matrix:")
    print(correlation_matrix)

    # sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    # plt.show()

    # Analyse strong correlations
    threshold = 0.95

    # Create a mask to identify strong correlations
    strong_correlations_mask = (abs(correlation_matrix) >= threshold) & (correlation_matrix < 1.0)

    # Plot the correlation matrix with strong correlations highlighted
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", mask=~strong_correlations_mask)
    plt.title("Correlation Matrix with Strong Correlations Highlighted")
    plt.show()

    return correlation_matrix


# Ranking Models
def rank_conn(fitness_results):
    fitness_values_df = pd.concat(fitness_results.values(), axis=1, keys=fitness_results.keys())

    model_avg_fitness = fitness_values_df.mean(axis=1)

    ranked_connectors = model_avg_fitness.sort_values(ascending=False)

    print("Ranked Connectors:")
    print(ranked_connectors)
    return ranked_connectors


# p values
def stat_test(fitness_results):
    algorithm_1 = list(fitness_results.keys())[0]
    algorithm_2 = list(fitness_results.keys())[1]

    fitness_values_df = pd.concat(fitness_results.values(), axis=1, keys=fitness_results.keys())

    p_values = {}
    for model in fitness_values_df.index:
        values_alg_1 = fitness_values_df.loc[model, (algorithm_1, slice(None))]
        values_alg_2 = fitness_values_df.loc[model, (algorithm_2, slice(None))]

        _, p_value = ttest_ind(values_alg_1, values_alg_2)
        p_values[model] = p_value

    print("P-values for t-test between", algorithm_1, "and", algorithm_2, ":")
    print(p_values)
    return p_values

def find_outliers(fitness_results):

    fitness_values_df = pd.concat(fitness_results.values(), axis=1, keys=fitness_results.keys())
    z_scores = zscore(fitness_values_df)

    # Set a threshold for considering a point as an outlier (e.g., Z-score > 3 or Z-score < -3)
    threshold = 3
    outliers_df = pd.DataFrame(abs(z_scores) > threshold, index=fitness_values_df.index, columns=fitness_values_df.columns)

    print("Outliers:")
    print(outliers_df)


fitness_results = get_fitness_results()
# Print the results
# for discovery_alg, values in fitness_results.items():
#     print(f"\nResults for {discovery_alg}:\n")
#     print("Mean:")
#     print(values["mean"])
#     print("\nStandard Deviation:")
#     print(values["std"])

# print(fitness_results)

correlation_matrix = cor_analysis(fitness_results)
ranked_connectors = rank_conn(fitness_results)
p_values = stat_test(fitness_results)
find_outliers(fitness_results)