# Working with a project as a contributor

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


## Evaluating code style

1. Running flake8:

   ```bash
   python -m flake8
   ```

1. Running pylint:

   ```bash
   pylint app.py config.py core_api/
   ```

## Deployment

### Deployment as a Python wheel

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


### Deployment as local Docker image

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

### Publishing Docker image

1. Build an image based on instructions above
2. Tag an image:
   ```bash
   docker tag dd6298653b37 demid5111/ldss-core-api:0.3
   ```
3. Login to the Dockerhub in terminal. Template command:
   ```bash
   docker login --username=USER
   ```
4. Publish an image on Dockerhub:
   ```bash
   docker push demid5111/ldss-core-api:0.3
   ```

### Publishing Docker image on Heroku

1. Make sure Heroku CLI is installed ([official documentation](https://devcenter.heroku.com/articles/getting-started-with-python#set-up))
2. Follow [official instructions](https://devcenter.heroku.com/articles/container-registry-and-runtime). First, login:
   ```bash
   heroku login
   ```
3. `heroku container:login`
4. `heroku create`
5. `docker tag demid5111/ldss-core-api:0.3 registry.heroku.com/ldss-core-api-app/web`
6. `docker push registry.heroku.com/ldss-core-api-app/web`
7. `heroku container:release web --app=ldss-core-api-app`

To see URL of application: `heroku domains --app ldss-core-api-app`.

To see logs of application: `heroku logs --app ldss-core-api-app`.

To enter remote machine: `heroku run bash -app ldss-core-api-app`.

To deploy: [link](https://stackoverflow.com/questions/71892543/heroku-and-github-items-could-not-be-retrieved-internal-server-error)

