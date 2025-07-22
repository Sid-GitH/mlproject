import sys
import os
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer 
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pandas as pd 
import numpy as np 

from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj


@dataclass 
class DataTransformationConfig:
    preprocesser_obj_file_path = os.path.join('artifact', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_data_transformer_object(self):
        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']

            numerical_pipeline = Pipeline(                                                  # transformers
                steps=[
                    ("imputer",SimpleImputer(strategy = "median")),
                    ("scaler",StandardScaler())
                ]
            )
            categorical_pipleine = Pipeline(
                steps=[
                ("imputer", SimpleImputer(strategy= "most_frequent")),
                ("one_hot_encoder",OneHotEncoder())
                
                ]
            )
            
            preprocessor = ColumnTransformer(                                                       # want to join nemerical and cat pipeline together as a single unit in transformer
                [
                ("numerical_pipeline",numerical_pipeline,numerical_columns),
                ("categorical_pipeline",categorical_pipleine, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data')
            logging.info('getting preprocessor object')

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = 'math_score'
            numerical_columns = ['writing_score', 'reading_score']

            input_feature_train_df = train_df.drop(columns=target_column_name,axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=target_column_name,axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info('applying preprocessor object of train dataset')

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[ 
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            save_obj(
                file_path=self.data_transformation_config.preprocesser_obj_file_path,
                obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocesser_obj_file_path
            )


        except Exception as e:
            raise CustomException(e,sys)

        






