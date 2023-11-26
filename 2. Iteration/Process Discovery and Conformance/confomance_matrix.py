import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import glob

def CreateMatrix(dataframe, name, includeHeatmap = False):
    """    
    Creates a matrix from a performance dictionary.
    Optionally generates heatmap png using matplotlib
    """
    df = dataframe
    

    #Save df to csv
    df.to_csv("conformance_matrix.csv", sep=",")

    if includeHeatmap:
        #Inspiration: https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
        row_titles = df.columns.values.tolist()
        row_titles = row_titles[1:]
        col_titles = df['Unnamed: 0'].tolist()
        
        #Remove first column
        df = df.drop(df.columns[0], axis=1)
        data = df.values
        
        fig, ax = plt.subplots()
        im = ax.imshow(data)
        ax.set_yticks(np.arange(len(row_titles)), labels=row_titles)
        ax.set_xticks(np.arange(len(col_titles)), labels=col_titles)


        for i in range(len(row_titles)):
            for j in range(len(col_titles)):
                ax.text(j, i, round(data[i, j],3), ha="center", va="center", color="w")
                
        ax.set_title("Conformance matrix:" + str(name))
        fig.tight_layout()
        plt.savefig(fname="conformance_matrix_heatmap.png")
        plt.show() 

def read_matrix():
    """    
    Reads a matrix from a csv file.
    """
    for filename in glob.glob(os.path.join('../Results', '*.csv')):
        matrix = pd.read_csv(filename)
        filename = os.path.splitext(os.path.basename(filename))[0]
        CreateMatrix(matrix, filename, True)


read_matrix()