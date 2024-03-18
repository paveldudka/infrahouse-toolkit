"""
.. topic:: ``ih-secrets list``

    A ``ih-secrets list`` subcommand.

    See ``ih-secrets list`` for more details.
"""
import sys
from logging import getLogger
from pprint import pformat

import click
from botocore.exceptions import ClientError
from tabulate import tabulate

LOG = getLogger(__name__)


def list_secrets(secretsmanager_client, all_fields=False):
    """
    Print a summary about EC2 instances in a region.
    """
    response = secretsmanager_client.list_secrets()
    LOG.debug("list_secrets() = %s", pformat(response, indent=4))
    secrets = []
    fields = ["Name", "Description"]
    if all_fields:
        fields.extend(["ARN", "CreatedDate", "LastAccessedDate", "LastChangedDate", "SecretVersionsToStages"])
    for secret in response["SecretList"]:
        row = []
        for field in fields:
            row.append(secret.get(field))
        secrets.append(row)

    print(tabulate(secrets, headers=fields, tablefmt="outline"))


@click.command(name="list")
@click.option("--all", help="Show all secret properties.", is_flag=True, default=False, show_default=True)
@click.pass_context
def cmd_list(ctx, **kwargs):
    """
    List created EC2 instances.
    """
    secretsmanager_client = ctx.obj["secretsmanager_client"]
    aws_config = ctx.obj["aws_config"]
    try:
        list_secrets(secretsmanager_client, kwargs["all"])
    except ClientError as err:
        LOG.exception(err)
        LOG.info("Try to run ih-secrets with --aws-profile option.")
        LOG.info("Available profiles:\n\t%s", "\n\t".join(aws_config.profiles))
        sys.exit(1)
