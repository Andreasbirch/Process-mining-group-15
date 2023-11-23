import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import zscore
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

discovery_algorithms = ["IM", "HM", "IMF", "DEC"]
# conformance_algorithms = ["token", "alignments"]
conformance_algorithms = ["token"]


def get_fitness_results():

    fitness_results = {}
    summary_results = {'mean': {}, 'std': {}}

    # Iterate through each discovery algorithm
    for discovery_alg in discovery_algorithms:

        if discovery_alg == "DEC":
            file_path = f"3. Iteration/Process Discovery/conformance_matrix.csv"
        else:
            file_path = f"2. Iteration/Results/output_{discovery_alg}_token.csv"

        df = pd.read_csv(file_path, index_col=0, decimal=',')  
        df = df.apply(lambda x: pd.to_numeric(x.str.replace(',', '.'), errors='coerce'))

        # print(df)
        mean_values = df.mean()
        std_values = df.std()

        summary_results['mean'][discovery_alg] = mean_values
        summary_results['std'][discovery_alg] = std_values

        fitness_results[discovery_alg] = df

    mean_df = pd.concat({f"{col}_mean": val for col, val in summary_results['mean'].items()}, axis=1)
    std_df = pd.concat({f"{col}_std": val for col, val in summary_results['std'].items()}, axis=1)

    combined_file_path = os.path.join("Results", "combined_mean_std_results.csv")
    combined_df = pd.concat([mean_df, std_df], axis=1)

    # Calculate overall mean for each column
    overall_mean = mean_df.mean()
    overall_mean.name = 'Overall_Mean'

    combined_df = pd.concat([combined_df, overall_mean.to_frame().transpose()])
    combined_df.to_csv(combined_file_path)

    return fitness_results, summary_results

# Correlation Analysis
def cor_analysis(fitness_results):

    # Separate fitness results for IM, HM, and IMF
    im_fitness = fitness_results['IM']
    hm_fitness = fitness_results['HM']
    imf_fitness = fitness_results['IMF']

    # Create correlation matrices for individual fitness results
    im_correlation_matrix = im_fitness.corr()
    hm_correlation_matrix = hm_fitness.corr()
    imf_correlation_matrix = imf_fitness.corr()

    plot_and_save_correlation_matrix(im_correlation_matrix, "IM Fitness")
    plot_and_save_correlation_matrix(hm_correlation_matrix, "HM Fitness")
    plot_and_save_correlation_matrix(imf_correlation_matrix, "IMF Fitness")

    # combined_fitness = pd.concat([im_fitness, hm_fitness, imf_fitness], axis=1)
    # combined_correlation_matrix = combined_fitness.corr()
    # plot_and_save_correlation_matrix(combined_correlation_matrix, "Combined Fitness")

    return im_correlation_matrix, hm_correlation_matrix, imf_correlation_matrix#, combined_correlation_matrix

def plot_and_save_correlation_matrix(correlation_matrix, title):

    # NOTE: can add a mask to only show strong correlations
    threshold = 0
    strong_correlations_mask = (abs(correlation_matrix) >= threshold) & (correlation_matrix < 1.0)

    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", mask=~strong_correlations_mask)
    plt.title(f"{title} - Correlation Matrix")
    # plt.show()
    plt.savefig(os.path.join("Results", f"{title}_correlation_matrix.png"))


# p values - statistical significance of the observed differences
# P can take any value between 0 and 1. Values close to 0 indicate that the observed difference is unlikely to be due to chance, whereas a P value close to 1 suggests no difference between the groups other than due to chance
# comparing the means of fitness values between two models
# A low p-value (typically less than 0.05) indicates that you can reject the null hypothesis that the means of the two models are equal
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4111019/#:~:text=The%20P%20value%20is%20defined,groups%20is%20due%20to%20chance.
def p_values(fitness_results):
    algorithm_1 = list(fitness_results.keys())[0]
    algorithm_2 = list(fitness_results.keys())[1]
    algorithm_3 = list(fitness_results.keys())[2]

    fitness_values_df = pd.concat(fitness_results.values(), axis=1, keys=fitness_results.keys())

    p_values = {}
    significant_p_values = {}

    for model in fitness_values_df.index:
        values_alg_1 = fitness_values_df.loc[model, (algorithm_1, slice(None))]
        values_alg_2 = fitness_values_df.loc[model, (algorithm_2, slice(None))]
        values_alg_3 = fitness_values_df.loc[model, (algorithm_3, slice(None))]

        _, p_value_1_2 = ttest_ind(values_alg_1, values_alg_2)
        _, p_value_1_3 = ttest_ind(values_alg_1, values_alg_3)
        _, p_value_2_3 = ttest_ind(values_alg_2, values_alg_3)

        p_values[model] = {
            f'{algorithm_1} vs {algorithm_2}': p_value_1_2,
            f'{algorithm_1} vs {algorithm_3}': p_value_1_3,
            f'{algorithm_2} vs {algorithm_3}': p_value_2_3
        }

        # Check if any p-value is less than 0.05
        if any(p_value < 0.05 for p_value in p_values[model].values()):
            significant_p_values[model] = p_values[model]

    p_values_df = pd.DataFrame(p_values)
    significant_p_values_df = pd.DataFrame(significant_p_values)

    # NOTE: it displays all the values if at least one value per connector was significant
    output_path = 'Results/p_values.csv'
    significant_p_values_df.to_csv(output_path, encoding='utf-8')

    print(f"Comparison values saved to {output_path}")

    return p_values_df


# Outliers represent instances where the process executions deviate significantly from the expected or modeled behavior according to the given discovery algorithms. 
def find_outliers(fitness_results):

    all_outliers_df = pd.DataFrame()

    for model_name, model_fitness in fitness_results.items():
        z_scores = zscore(model_fitness)

        threshold = 3
        outliers_df = pd.DataFrame(abs(z_scores) > threshold, index=model_fitness.index, columns=model_fitness.columns)

        # Filter and display only the rows where at least one value is TRUE
        filtered_outliers = outliers_df[outliers_df.any(axis=1)]

        print(f"Filtered Outliers for {model_name}:")
        print(filtered_outliers)

        filtered_outliers['Model'] = model_name  # Add a column for the model name
        all_outliers_df = pd.concat([all_outliers_df, filtered_outliers])

    all_outliers_df.to_csv('Results/all_outliers_combined.csv', encoding='utf-8', index=True)

    return all_outliers_df

def get_best_connectors(fitness_results):

    im_fitness = fitness_results['IM']
    hm_fitness = fitness_results['HM']
    imf_fitness = fitness_results['IMF']
    dec_fitness = fitness_results['DEC']
    print(dec_fitness)
    data = [im_fitness, hm_fitness, imf_fitness, dec_fitness]
    result_df = pd.DataFrame(index=dec_fitness.index)
    for model, d in zip(['IM', 'HM', 'IMF', 'DEC'], data):

        # Rank each column individually
        df_ranked = d.rank(ascending=True, axis=0)
        sum_ranked_values = df_ranked.sum(axis=1).sort_values(ascending = False) 
        result_df = pd.concat([result_df, d, df_ranked, sum_ranked_values], axis=1)

        # print(im_fitness)
        # print(df_ranked)
        # print(sum_ranked_values)
        # print(sum_sorted_by_fitness)

    result_df.to_csv('Results/Best_connectors.csv', index=False)

    return result_df

def calculate_accuracy(fitness_df):
    correct_count = 0
    total_count = 0
    top_n = 3

    for col in fitness_df.columns:
        diagonal_value = fitness_df.at[col, col]
        # Highest fitness from each column
        # max_column_value = fitness_df[col].max()
        
        top_n_values = fitness_df[col].nlargest(top_n).values
        
        if diagonal_value in top_n_values:
            correct_count += 1
            # print(col)
        total_count += 1

    # print(correct_count, total_count)
    accuracy_percentage = (correct_count / total_count) * 100
    return accuracy_percentage

def analyse_diagonal_percentage(fitness_results):
    results = {}

    for connector, fitness_df in fitness_results.items():
        accuracy_percentage = calculate_accuracy(fitness_df)
        results[connector] = accuracy_percentage

    result_df = pd.DataFrame(list(results.items()), columns=['Model', 'Accuracy_Percentage'])
    result_df.to_csv('Results/diagonal_accuracy.csv', index=False)

    return result_df


# Running data analysis functions

fitness_results, summary_results = get_fitness_results()
# get_best_connectors(fitness_results)
# analyse_diagonal_percentage(fitness_results)

# Print mean and std values. Same values are saved to CSV file
# for discovery_alg, mean_values in summary_results['mean'].items():
#     print(f"Mean values for {discovery_alg}:")
#     print(mean_values)
# for discovery_alg, std_values in summary_results['std'].items():
#     print(f"Standard deviation values for {discovery_alg}:")
#     print(std_values)


# correlation_matrix = cor_analysis(fitness_results)
# p_values = p_values(fitness_results)
# find_outliers(fitness_results)



# column wise -> top 3

