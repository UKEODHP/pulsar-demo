# Pulsar Demo for EO DataHub Project

An example of how to publish and subscribe to a Pulsar message queue.

## Install Dependencies

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Execution

To see the help docs, `python -m pulsar_demo`.

The following examples expect you to have a Pulsar message broker running on 127.0.0.1:6650.

### Subscribe

```bash
python -m pulsar_demo pulsar://127.0.0.1:6650 pulsar-demo subscribe --prefix sub1
```

### Publish

```bash
python -m pulsar_demo pulsar://127.0.0.1:6650 pulsar-demo publish --prefix pub1
```
