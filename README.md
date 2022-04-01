# ldss-core-api

## Development

1. Running flake8:

   ```bash
   python -m flake8
   ```

1. Running pylint:

   ```bash
   pylint app.py config.py core_api/
   ```

## Deployment

1. Build wheels:

   ```bash
   python -m build
   ```

1. Install locally (optional) to check:

   ```bash
   pip install -e .
   ```
   
   OR
   
   ```bash
   pip install --force-reinstall dist/core_api_flask_seed-0.0.1-py3-none-any.whl
   ```

1. Export needed variables (optional) to check:
   
   ```bash
   export FLASK_APP=core_api
   export FLASK_ENV=development
   ```

1. Run (optional) to check:

   ```bash
   flask run
   ```
   
## Running from sources

1. Clone the repository

2. Download the released version of the Decision Maker, currently supported version is 
   `https://github.com/ldss-hse/ldss-core-aggregator/releases/download/decision_maker_v0.3/lingvo-dss-all.jar` 
   and put it into 
   `core_api/core_api/async_tasks/decision_maker/scripts/bin/` folder.

3. Run the web server:

   ```bash
   python core_api/core_api/app.py
   ```

4. Run task executor:

   ```bash
   python core_api/core_api/async_tasks/huey_consumer.py
   ```

## Running as a local Docker container

1. Build fresh image:
   ```bash
    docker build --tag core_api .
   ```
   If you want to debug your build, make sure you have disabled a setting in Docker Desktop:
   ```json
   {
      "features": {
          "buildkit": false
      }  
   }
   ```

2. Run image by creating a container:
   ```bash
   docker run -p 1234:5000 -it core_api
   ```

3. Debug container during the build
   ```bash
   docker run --rm -it 94048487087a bash
   ```
   
## Working with Decision Maker as a service

You need to make a request to the URL where it is running, for example for local use case you need to send
POST request to `http://localhost:1234/api/v1/make-decision` and as a payload send a dictionary:

```json
{
   "task_description": <HERE GOES JSON with description>
}
```

Example of such a JSON file is present in 
[./core_api/core_api/async_tasks/decision_maker/scripts/bin/description_multilevel.json](./core_api/core_api/async_tasks/decision_maker/scripts/bin/description_multilevel.json).

Example Python code that demonstrates how to make a request is present in 
[./core_api/demo/demo_request.py](./core_api/demo/demo_request.py), example Javascript code is present in
[./core_api/core_api/templates/index.html)](./core_api/core_api/templates/index.html) 
(function`postNewMakeDecisionTask`).
