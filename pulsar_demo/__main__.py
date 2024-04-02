from random import choice
from string import ascii_uppercase
from time import sleep
from typing import Optional

import click
import pulsar
import pulsar.exceptions

INTERVAL = 1


@click.group()
@click.argument("pulsar_url", type=str)
@click.argument("topic", type=str)
@click.pass_context
def cli(ctx, pulsar_url: str, topic: str):
    ctx.ensure_object(dict)
    ctx.obj["CLIENT"] = pulsar.Client(pulsar_url)
    ctx.obj["TOPIC"] = topic
    click.echo(f"Connecting to broker '{pulsar_url}' with topic '{topic}'")


@cli.command()
@click.option("--prefix", type=str, default=None)
@click.option("-n", type=int, default=100, show_default=True)
@click.pass_context
def publish(ctx, prefix: Optional[str] = None, n: Optional[int] = 100):
    """
    Publish n messages to Pulsar broker.
    """
    prefix = prefix or "".join(choice(ascii_uppercase) for _ in range(6))
    client: pulsar.Client = ctx.obj["CLIENT"]
    topic: str = ctx.obj["TOPIC"]
    producer: pulsar.Producer = client.create_producer(topic=topic, producer_name=prefix)
    try:
        for ii in range(n):
            msg = f"{prefix}-{ii}"
            click.echo(msg)
            producer.send(msg.encode("utf-8"))
            sleep(INTERVAL)
    finally:
        producer.close()
        client.close()


@cli.command()
@click.option("--prefix", type=str, default=None)
@click.option("-n", type=int, default=100, show_default=True)
@click.pass_context
def subscribe(ctx, prefix: Optional[str] = None, n: Optional[int] = 100):
    """
    Subscribe to n messages from a Pulsar broker.
    """
    prefix = prefix or "".join(choice(ascii_uppercase) for _ in range(6))
    client: pulsar.Client = ctx.obj["CLIENT"]
    topic: str = ctx.obj["TOPIC"]
    consumer = client.subscribe(topic=topic, subscription_name=prefix)
    try:
        for _ in range(n):
            msg = consumer.receive()
            click.echo(msg.data())
            consumer.acknowledge(msg)
    except pulsar.exceptions.Interrupted:
        pass
    except Exception:
        consumer.negative_acknowledge(msg)
    finally:
        consumer.close()
        client.close()


if __name__ == "__main__":
    cli(obj={})
