import datetime
import json
import logging
import time
import os
import sys

import boto3
import schedule

import shared.log_config
import watcher_admin
import watcher_worker

AWS_REGION=os.environ['AWS_REGION']
ADMIN_LOG_FILE = 'watcher-admin.log'
WORKER_LOG_FILE = 'watcher-worker.log'
ADMIN_MODE = 'admin'
WORKER_MODE = 'worker'


# todo: get rid of this
def log_event(cw):
  # todo: get metric info right
  resp = cw.put_metric_data(
    Namespace = "JWang Test",
    MetricData = [
      {
        'MetricName': 'test metric name',
        'Timestamp': datetime.datetime.now(),
        'Value': 1
      }
    ]
  )


def check_args():
  assert len(sys.argv) > 1, 'cmd needs to specify worker or admin'
  assert sys.argv[1] in [WORKER_MODE, ADMIN_MODE], 'mode not supported: %s' % sys.argv[1]


def get_run_mode():
  return sys.argv[1]


def set_logging(mode):
  assert mode in [WORKER_MODE, ADMIN_MODE]
  logging.basicConfig(
    filename='watcher-%s.log' % mode,
    level=shared.log_config.LOG_LEVEL)


if __name__ == '__main__':

  check_args()
  run_mode = get_run_mode()
  set_logging(run_mode)

  if run_mode == ADMIN_MODE:
    watcher_admin.run()
  elif run_mode == WORKER_MODE:
    watcher_worker.run()

  # cw = boto3.client('cloudwatch', region_name=AWS_REGION)

  # schedule.every(5).seconds.do(log_event, cw)

  # while True:
  #   schedule.run_pending()
  #   time.sleep(1)
