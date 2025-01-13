from flask import Blueprint, jsonify, request
import pandas as pd
from .models import DatasetManager
import json
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA

bp = Blueprint('main', __name__)
dataset = None


def findTime(df, timepoint):
    return df.loc[df['TIMEPOINT'] == timepoint]

def one_hot_encode_non_numerical(df):
    non_numerical_cols = df.select_dtypes(include=['object', 'category']).columns

    df_encoded = pd.get_dummies(df, columns=non_numerical_cols, dtype=float)
    
    return df_encoded

def pca_to_2d(df):
    numeric_df = one_hot_encode_non_numerical(df)

    # Compute PCA
    pca = PCA(n_components=2)
    pca_results = pca.fit_transform(numeric_df)

    # Extract PCA1 and PCA2
    pca1 = pca_results[:, 0].tolist()
    pca2 = pca_results[:, 1].tolist()

    # Save PCA results as a dictionary
    pca_data = {
        'pca1': pca1,
        'pca2': pca2,
        # 'klg': df['KLG'].astype(str).tolist()
    }
    return pca_data

def to_2d(df,var1, var2):
    numeric_df = one_hot_encode_non_numerical(df)
    print(var1)

    pca_data = {
        'pca1': numeric_df[var1].tolist(),
        'pca2': numeric_df[var2].tolist()
    }
    return pca_data


@bp.route('/data', methods = ['GET'])
def get_dataset():
    global dataset
    try:
        # Load dataset if not already loaded
        if dataset is None:
            dataset = pd.read_csv('../ZIB_demoFeatures_v00_507.csv')
        # Convert DataFrame to list of dictionaries
        return dataset.to_json(orient="records")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/scatter', methods = ['GET'])
def get_scatter():
    global dataset
    try:
        if dataset is None:
            dataset = pd.read_csv('../ZIB_demoFeatures_v00_507.csv')

        x_var = request.args.get('var1')
        y_var = request.args.get('var2')
        if x_var and y_var:
            #return {'a': 'OK'}
            scatter = to_2d(dataset.dropna().copy(),x_var,y_var)
        else:
            scatter = pca_to_2d(dataset.dropna().copy())
        return scatter

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    