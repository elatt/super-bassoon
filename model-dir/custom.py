"""
Copyright 2021 DataRobot, Inc. and its affiliates.
All rights reserved.
This is proprietary source code of DataRobot, Inc. and its affiliates.
Released under the terms of DataRobot Tool and Utility Agreement.
"""
from datarobot_drum import RuntimeParameters


def mask(value, visible=3):
    return value[:visible] + ("*" * len(value[visible:]))


def transform(data, model):
    print("Loading the following Runtime Parameters:")
    option1 = RuntimeParameters.get("option1")
    option2 = RuntimeParameters.get("option2")
    option3 = RuntimeParameters.get("option3")
    print(f"\toption1: {option1}")
    print(f"\toption2: {option2}")
    print(f"\toption3: {option3}")

    credential = RuntimeParameters.get("api_key")
    if credential is not None:
        credential_type = credential.pop("credentialType")
        print(
            f"\tapi_key(type={credential_type}): "
            + str({k: mask(v) for k, v in credential.items()})
        )
    else:
        print("No credential data set")
    return data
