# Autoblocks Replays

## Replaying Locally

Start the application with replays enabled:

```bash
AUTOBLOCKS_REPLAYS_ENABLED=true poetry run start
```

In another terminal, set the `AUTOBLOCKS_API_KEY` environment variable:

```bash
export AUTOBLOCKS_API_KEY=my-api-key
```

Then replay traces from a view:

```bash
poetry run replay \
  --view-id clkeamsei0001l908cmjjtqrf \
  --num-traces 3
```

```
################################################################################
Your replay id is 2023-07-23_09-36-36
################################################################################

Replaying event {'id': 'geepag24zence2kbe0ppagt9', 'traceId': '7cb3ec98-b320-4e62-9a51-b15d0218ae4c', 'timestamp': '2023-07-22T18:32:51.862Z', 'message': 'request.payload', 'properties': {'payload': {'query': 'What are all of the airports in London?'}, 'source': 'DEMO_REPLAYS'}}
```

The original and replayed traces are written to the `autoblocks-replays/` folder with the structure:

```
autoblocks-replays/
    <replay-id>/
        <trace-id>/
            original/
                <event-number>-<message>.json
            replayed/
                <event-number>-<message>.json
```

<img width="981" alt="Screenshot 2023-07-23 at 10 06 39 AM" src="https://github.com/autoblocksai/actions/assets/7498009/ce20918f-ce75-4cd3-a5d2-66d3e1a00914">

Inspect the original vs replayed output manually or use a CLI tool like `diff` to surface differences:

```
diff \
  autoblocks-replays/2023-07-23_09-36-36/7cb3ec98-b320-4e62-9a51-b15d0218ae4c/original \
  autoblocks-replays/2023-07-23_09-36-36/7cb3ec98-b320-4e62-9a51-b15d0218ae4c/replayed
```

<img width="799" alt="Screenshot 2023-07-22 at 2 39 47 PM" src="https://github.com/autoblocksai/actions/assets/7498009/4279db15-26fc-4346-8e16-1ed060bcd9f7">

## Replaying in GitHub Actions

Use the [`autoblocksai/actions/replay`](https://github.com/autoblocksai/actions/tree/main/replay) action to replay events in a GitHub Actions workflow. This is similar to replaying events locally but allows you to automate replays in your CI workflow and view results in the GitHub UI.

The action will leave a comment on your commit with a summary of the replay results:

<img width="785" alt="Screenshot 2023-07-23 at 11 49 25 AM" src="https://github.com/autoblocksai/actions/assets/7498009/b6507fde-9a04-4c4d-9049-2bdefb35f933">

You can view diffs of individual events or entire traces:

<img width="1159" alt="Screenshot 2023-07-23 at 11 02 18 AM" src="https://github.com/autoblocksai/actions/assets/7498009/80055f36-a310-4056-8ac3-f2f0e4ac2b3f">
