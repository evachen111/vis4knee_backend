from flask import Blueprint, jsonify, request
import pandas as pd
from .models import DatasetManager

bp = Blueprint('main', __name__)
dataset = None

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