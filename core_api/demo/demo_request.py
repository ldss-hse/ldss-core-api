import json
import random
from pathlib import Path

import requests

from core_api.constants import CORE_PATH


def _create_random_weights():
    random_weight = round(random.uniform(0.1, 0.7), ndigits=1)
    print(f'Random weight is {random_weight}')
    return {
        '1': random_weight,
        '2': round(1 - random_weight, ndigits=1)
    }


def construct_payload_from_gold_pure_description(weights):
    gold_asset_path = CORE_PATH / 'async_tasks' / 'decision_maker' / 'scripts' / 'bin' / 'description_multilevel.json'

    with gold_asset_path.open(encoding='utf-8') as f:
        task_description_multilevel = json.load(f)

    task_description_multilevel['expertWeightsRule'] = weights

    return {
        'task_description': task_description_multilevel
    }


def construct_payload_from_test_file(weights):
    gold_asset_path = Path(r'C:\Users\demidovs\Downloads\testJSON1.json')
    if not gold_asset_path.exists():
        raise ValueError('Path to JSON file should exist')

    with gold_asset_path.open(encoding='utf-8') as f:
        payload = json.load(f)

    payload['task_description']['expertWeightsRule'] = weights

    return payload


def make_request_to_service(url, payload):
    headers = {
        "content-type": "application/json"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    return response.json()


def check_response(response_json, expected_weights):
    print(f'Received weights: {response_json["taskResult"]["expertWeightsRule"]}')
    err_msg = 'Weights are not the same. Does decision maker really consider a not hardcoded example?'
    assert response_json["taskResult"]["expertWeightsRule"] == expected_weights, err_msg
    assert response_json["taskResult"]["alternativesOrdered"], 'Decision Maker cannot return empty list of alternatives'


def main():
    host_to_call = 'http://localhost:5000'
    # host_to_call = 'https://ldss-core-api-app.herokuapp.com'
    api_endpoint = '/api/v1/make-decision'
    url_to_call = f'{host_to_call}{api_endpoint}'
    print(f'Calling {url_to_call}')

    print('Checking from pure description...')
    weights = _create_random_weights()
    print(f'New weights: {weights}')
    payload = construct_payload_from_gold_pure_description(weights=weights)
    result = make_request_to_service(url_to_call, payload)
    check_response(result, weights)
    print('Checks passed')

    print('Checking from test payload...')
    weights = _create_random_weights()
    print(f'New weights: {weights}')
    payload = construct_payload_from_test_file(weights=weights)
    result = make_request_to_service(url_to_call, payload)
    check_response(result, weights)
    print('Checks passed')


if __name__ == '__main__':
    main()
