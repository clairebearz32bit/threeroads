import pandas as pd
import numpy as np
import random
import re
import gc
import os
from fuzzywuzzy import fuzz


JEOPARDY_ROUND = list('$' + str(i) for i in range(200, 1001, 200))
DOUBLE_JEOPARDY = list('$' + str(i) for i in range(400, 2001, 400))


class Trivia:
    def __init__(self, file_path='../datasets/trivia.tsv'):
        if file_path not in os.listdir(os.getcwd()):
            raise FileNotFoundError(f'Dataset {file_path} not found.')

        file_ext = file_path.split('.')[-1]

        if not file_ext.endswith(('csv', 'tsv')):
            raise Exception('Dataset must be a delimiter seperated file.')

        if file_ext.endswith('tsv'):
            self.clues = self.get_df_from_file(file_path, sep='\t')

        else:
            self.clues = self.get_df_from_file(file_path)


    def is_dataset_valid(self):
        valid = True

        if not {'Value', 'Category', 'Question', 'Answer'}.issubset(set(self.clues.columns.values)):
            valid = False



        return valid


    @staticmethod
    def get_df_from_file(path, sep=','):
        # Load the trivia clues from file path

        df = pd.read_csv(path, sep=sep)
        df = pd.DataFrame(df)
        # Strip whitespace from column names
        df.columns = df.columns.str.replace(' ', '')
        return df

    # Takes a df parameter so that custom filters can be passed such as specific values and categories before indexing.
    # Uses np.random.choice instead of pd.sample() due to much faster speed.
    def get_random(self, df=None):
        if df is None:
            df = self.clues

        arr = df.loc[:, ['Value', 'Category', 'Question', 'Answer']]
        return arr.loc[np.random.choice(arr.index, replace=False)]

    def get_random_by_value(self, value):
        if value not in list(range(1,11)):
            raise ValueError("Value must be in range.")

        else:
            return self.get_random(self.clues.loc[self.clues['Value'] == value])

    def get_by_category(self, category):
        if category.upper() in self.clues['Category'].to_string():
            return self.get_random(self.clues.loc[self.clues['Category'] == category.upper()])


if __name__ == '__main__':
    trivia = Trivia('../datasets/trivia.tsv')
    df = trivia.clues.dropna()

    #
    # df.loc[(df['Value'] != 0), 'Value'] = pd.to_numeric(df.loc[df['Value'] != 0, 'Value'].replace('[$,]', '', regex=True))
    # # df.loc[df['Value'], 'Value'] = df.loc[df['Value'], 'Value'].to_numeric()
    # for col in df['Value'].unique():
    #     print(col)
    # print(df['Value'].head().dtype)
    # # values = df['Value']
    # # print(values.head())
    # # values = values.astype(int)