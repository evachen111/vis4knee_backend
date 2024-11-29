import pandas as pd
from flask import current_app

class DatasetManager:
    _dataset = None
    
    @classmethod
    def get_dataset(cls):
        """
        Load dataset if not already loaded, using the path from config
        """
        if cls._dataset is None:
            try:
                cls._dataset = pd.read_csv(current_app.config['DATASET_PATH'])
            except Exception as e:
                current_app.logger.error(f"Error loading dataset: {e}")
                return None
        return cls._dataset
    
    @classmethod
    def process_selected_points(cls, points):
        """
        Process selected points 
        Add your specific data processing logic here
        """
        dataset = cls.get_dataset()
        if dataset is not None:
            # Example: Filter dataset based on selected points
            selected_data = dataset.iloc[points]
            return selected_data.to_dict(orient='records')
        return None