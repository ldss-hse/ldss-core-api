import json
import random

import requests

from core_api.constants import CORE_PATH


def main():
    host_to_call = 'http://localhost:1234'
    api_endpoint = '/api/v1/make-decision'
    url_to_call = f'{host_to_call}{api_endpoint}'
    print(f'Calling {url_to_call}')

    gold_asset_path = CORE_PATH / 'async_tasks' / 'decision_maker' / 'scripts' / 'bin' / 'description_multilevel.json'
    with gold_asset_path.open(encoding='utf-8') as f:
        task_description_multilevel = json.load(f)

    random_weight = round(random.uniform(0.1, 0.7), ndigits=1)
    print(f'Random weight is {random_weight}')
    task_description_multilevel['expertWeightsRule'] = {
        '1': random_weight,
        '2': round(1 - random_weight, ndigits=1)
    }
    print(f'New weights: {task_description_multilevel["expertWeightsRule"]}')

    payload = {
        'task_description': task_description_multilevel
    }
    headers = {
        "content-type": "application/json"
    }
    response = requests.post(url_to_call, data=json.dumps(payload), headers=headers)

    result = response.json()

    print(f'Received weights: {result["taskResult"]["expertWeightsRule"]}')

    err_msg = 'Weights are not the same. Does decision maker really consider a not hardcoded example?'
    assert result["taskResult"]["expertWeightsRule"] == task_description_multilevel["expertWeightsRule"], err_msg


if __name__ == '__main__':
    main()
