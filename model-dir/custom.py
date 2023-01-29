"""
Copyright 2023 DataRobot, Inc. and its affiliates.
All rights reserved.
This is proprietary source code of DataRobot, Inc. and its affiliates.
Released under the terms of DataRobot Tool and Utility Agreement.
"""
from datarobot_drum.runtime_parameters.runtime_parameters import RuntimeParameters
import pandas as pd
import requests

# Load runtime params set by the platform
PUBLIC_API_URL = RuntimeParameters.get('DATAROBOT_ENDPOINT') + '/api/v2'
API_KEY = RuntimeParameters.get('DATAROBOT_API_KEY')['password']
DEPLOYMENT_ID = RuntimeParameters.get('deploymentID')

# Will be set
API_URL = None
DATAROBOT_KEY = None

# Don't change this. It is enforced server-side too.
MAX_PREDICTION_FILE_SIZE_BYTES = 52428800  # 50 MB


class DataRobotPredictionError(Exception):
    """Raised if there are issues getting predictions from DataRobot"""


def make_datarobot_deployment_predictions(data, deployment_id):
    """
    Make predictions on data provided using DataRobot deployment_id provided.
    See docs for details:
         https://app.datarobot.com/docs/predictions/api/dr-predapi.html

    Parameters
    ----------
    data : str
        If using CSV as input:
        Feature1,Feature2
        numeric_value,string

        Or if using JSON as input:
        [{"Feature1":numeric_value,"Feature2":"string"}]

    deployment_id : str
        The ID of the deployment to make predictions with.

    Returns
    -------
    Response schema:
        https://app.datarobot.com/docs/predictions/api/dr-predapi.html#response-schema

    Raises
    ------
    DataRobotPredictionError if there are issues getting predictions from DataRobot
    """
    # Set HTTP headers. The charset should match the contents of the file.
    headers = {
        # As default, we expect CSV as input data.
        # Should you wish to supply JSON instead,
        # comment out the line below and use the line after that instead:
        'Content-Type': 'text/plain; charset=UTF-8',
        # 'Content-Type': 'application/json; charset=UTF-8',

        'Authorization': 'Bearer {}'.format(API_KEY),
        'DataRobot-Key': DATAROBOT_KEY,
    }

    url = API_URL.format(deployment_id=deployment_id)

    # Prediction Explanations:
    # See the documentation for more information:
    # https://app.datarobot.com/docs/predictions/api/dr-predapi.html#request-pred-explanations
    # Should you wish to include Prediction Explanations or Prediction Warnings in the result,
    # Change the parameters below accordingly, and remove the comment from the params field below:

    params = {
        # If explanations are required, uncomment the line below
        # 'maxExplanations': 3,
        # 'thresholdHigh': 0.5,
        # 'thresholdLow': 0.15,
        # For multiclass/clustering explanations only one of the 2 fields below may be specified
        # Explain this number of top predicted classes in each row
        # 'explanationNumTopClasses': 1,
        # Explain this list of class names
        # 'explanationClassNames': [],
        # If text explanations are required, uncomment the line below.
        # 'maxNgramExplanations': 'all',
        # Uncomment this for Prediction Warnings, if enabled for your deployment.
        # 'predictionWarningEnabled': 'true',
    }
    # Make API request for predictions
    predictions_response = requests.post(
        url,
        data=data,
        headers=headers,
        # Prediction Explanations:
        # Uncomment this to include explanations in your prediction
        # params=params,
    )
    _raise_dataroboterror_for_status(predictions_response)
    # Return a Python dict following the schema in the documentation
    return predictions_response.json()


def _raise_dataroboterror_for_status(response):
    """Raise DataRobotPredictionError if the request fails along with the response returned"""
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        err_msg = '{code} Error: {msg}'.format(
            code=response.status_code, msg=response.text)
        raise DataRobotPredictionError(err_msg)


### PASTE AN INTEGRATION SNIPPET FROM A DEPLOYMENT ABOVE ###
def load_model(code_dir):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer {}'.format(API_KEY),
    }
    return object()  # model placeholder


def score(data, model, **kwargs):
    # prepare the prediction request payload
    payload = data.to_csv(index=False)

    # make the prediction request
    response = make_datarobot_deployment_predictions(payload, DEPLOYMENT_ID)

    # convert the prediction request response to the required data structure
    predictions = [item['prediction'] for item in response['data']]
    predictions_data = pd.DataFrame({'Predictions': predictions})

    return predictions_data
