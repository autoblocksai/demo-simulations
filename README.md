# Autoblocks Simulations

This repository contains an example project that integrates Autoblocks Simulations into a Python application
via GitHub Actions.
See the [documentation](https://docs.autoblocks.ai/guides/simulations) for more information.

## Instructions

### 1. Install dependencies

```bash
poetry install
```

### 2. Start the application

Start the application with your simulation ingestion key,
a simulation id to uniquely identify your simulation run,
and any other environment variables needed to run your application:

```bash
AUTOBLOCKS_INGESTION_KEY=<simulation-ingestion-key> \
AUTOBLOCKS_SIMULATION_ID=$(date +%Y%m%d%H%M%S) \
OPENAI_API_KEY=<openai-api-key> \
poetry run start
```

### 3. Run the simulation

In another terminal, run either:

* `simulation-static`, which will replay a static set of test cases against your application:

```bash
poetry run simulation-static
```

* `simulation-production-replay`, which will replay a set of production events fetched from the Autoblocks API:

```bash
AUTOBLOCKS_API_KEY=<autoblocks-api-key> poetry run simulation-production-replay
```
