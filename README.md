# Autoblocks Simulations

This repository contains an example project that integrates Autoblocks Simulations into a Python application
via GitHub Actions.
See the [documentation](https://docs.autoblocks.ai/guides/simulations) for more information.

## Instructions for running locally

### 1. Install dependencies

```bash
poetry install
```

### 2. Run the tests

Set the `AUTOBLOCKS_INGESTION_KEY` environment variable to your simulation ingestion key before running the tests
so that any events sent during the test run are sent as simulated events.

```bash
AUTOBLOCKS_INGESTION_KEY=<simulation-ingestion-key> \
OPENAI_API_KEY=<openai-api-key> \
poetry run pytest
```

[View your simulation](https://app.autoblocks.ai/simulations)

### 3. Run a simulation with production events

To run a simulation that replays production events, first start the application:

```bash
AUTOBLOCKS_INGESTION_KEY=<simulation-ingestion-key> \
AUTOBLOCKS_SIMULATION_ID=$(date +%Y%m%d%H%M%S) \
OPENAI_API_KEY=<openai-api-key> \
poetry run start
```

Then, in a separate terminal, run the simulation:

```bash
AUTOBLOCKS_API_KEY=<autoblocks-api-key> poetry run simulation-production-replay
```

[View your simulation](https://app.autoblocks.ai/simulations)
