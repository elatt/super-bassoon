"""
Copyright 2021 DataRobot, Inc. and its affiliates.
All rights reserved.
This is proprietary source code of DataRobot, Inc. and its affiliates.
Released under the terms of DataRobot Tool and Utility Agreement.
"""
from datarobot_drum import RuntimeParameters


def mask(value):
    return value[:2] + ('*'*len(value[2:]))


def transform(data, model):
    print("Loading the following Runtime Parameters:")
    option1 = RuntimeParameters.get('option1')
    option2 = RuntimeParameters.get('option2')
    print(f"\toption1: {option1}")
    print(f"\toption2: {option2}")
    
    credential = RuntimeParameters.get('api_key')
    if credential is not None:
        credential_type = credential.pop('credentialType')
        print(f"\tapi_key(type={credential_type}): " + credential)
    else:
        print("No credential data set")
    return data
