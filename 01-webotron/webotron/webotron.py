#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Webotron: Deploy websites with AWS
It automates the process of deploying static websites on AWS
Features:
- Configure AWS S3 buckets
- Create them
- Set them up for static website hosting
"""

from pathlib import Path

import boto3
from botocore.exceptions import ClientError
import click

from bucket import BucketManager

session = boto3.Session()
bucket_manager = BucketManager(session)


@click.group()
def cli():

    """Webotron deploys websites to AWS"""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets"""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an s3 bucket"""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket_name')
def setup_bucket(bucket_name):
    """Create and configure S3 bucket"""

    s3_bucket = bucket_manager.init_bucket(bucket_name)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET"""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
