# Get necessary imports
import os
import json
import pandas as pd

# Get the data

def append_ground_truth(truth_df, dataset_name):
    # Check if id has already been added to the dataframe
    if dataset_name in truth_df['dataset_name'].values:
        return truth_df
    
    # Loop over the datapoint directories
    datapoint_dir = f'/Users/michaelscott/Documents/GitHub/datagen-repo/data/{dataset_name}/'
    for datapoint_id in os.listdir(datapoint_dir):
        datapoint_path = os.path.join(datapoint_dir, datapoint_id)
        if not os.path.isdir(datapoint_path):
            continue

        # Extract the dataset name and ID from the datapoint path
        dataset_name = os.path.basename(os.path.dirname(datapoint_path))
        datapoint_id = os.path.basename(datapoint_path)

        # Load the JSON data from the datapoint request file
        datapoint_file = os.path.join(datapoint_path, 'datapoint_request.json')
        with open(datapoint_file, 'r') as f:
            data = json.load(f)

        # Load the actor metadata from the actor_metadata.json file
        metadata_file = os.path.join(datapoint_path, 'actor_metadata.json')
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        # Extract the age range, ethnicity, and gender from the actor metadata
        age_range = metadata['identity_label']['age']
        ethnicity = metadata['identity_label']['ethnicity']
        gender = metadata['identity_label']['gender']
        demographics = {'gender': gender, 'age_range': age_range, 'ethnicity': ethnicity}

        # Extract the emotion data from the JSON data
        emotion = {}
        for datapoint in data['datapoints']:
            expression = datapoint['human']['head']['expression']['name']
            intensity = datapoint['human']['head']['expression']['intensity']
            emotion = {'expression': expression, 'intensity': intensity}

        # Concatenate the demographic and emotion information into a single dictionary
        data_dict[datapoint_id] = {'dataset_name': dataset_name, 'id': datapoint_id}
        data_dict[datapoint_id].update(demographics)
        data_dict[datapoint_id].update(emotion)

    # Add data to the truth_df using pd concat
    truth_df = pd.concat([truth_df, pd.DataFrame.from_dict(data_dict, orient='index')])

    return truth_df