# `ldss-core-api`: REST API for Linguistic multi-level decision-making

This component is distributed as a [Docker image](https://hub.docker.com/r/demid5111/ldss-core-api)

There are several ways to use the API:

1. [Building and running from sources](./CONTRIBUTING.md)
2. Running as a PyPi package (currently WIP)
3. [Building and running as a local Docker container](./CONTRIBUTING.md)
4. [Pulling and running released Docker image (recommended)](#pull)
5. Accessing a remotely started Docker container (currently not available)
   
## Pulling and running released Docker image (recommended) <a name="pull></a>

1. Install Docker Desktop on your system ([official instructions](https://docs.docker.com/desktop/))
2. Pull the image:
   ```bash
   docker pull demid5111/ldss-core-api:0.3
   ```
3. Run the image:
   ```bash
   docker run -p 1234:5000 --name core_api -it demid5111/ldss-core-api:0.3
   ```
4. Proceed to section **Working with Decision Maker as a service** with `127.0.0.1:1234` as a service URL


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
