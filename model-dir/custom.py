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
    credential = RuntimeParameters.get('api_key')
    assert credential['credentialType'] == 'basic'

    option1 = RuntimeParameters.get('option1')
    option2 = RuntimeParameters.get('option2')
    print("Loading the following Runtime Parameters:")
    print(f"\toption1: {option1}")
    print(f"\toption2: {option2}")
    print(f"\tapi_key: username={mask(credential['username'])} "
          f"password={mask(credential['password'])}")
    return data
