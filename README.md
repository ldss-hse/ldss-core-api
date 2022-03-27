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

1. Run the web server:

   ```bash
   python core_api/core_api/app.py
   ```

1. Run task executor:

   ```bash
   python core_api/core_api/async_tasks/huey_consumer.py
   ```
