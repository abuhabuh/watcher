"""Watcher admin instance
"""
import os
import time


# todo: config this
CONFIG_FILE_DIR = os.environ['CONFIG_FILE_DIR']
# todo: set actual interval
# REFRESH_INTERVAL_SEC = 60
REFRESH_INTERVAL_SEC = 1


class WatcherAdmin:
  """
  TODO: check out Dask.distributed -- https://distributed.readthedocs.io/en/latest/

  - admin maintains (check, worker) pair and ensure functioning
  - admin sees worker that's unreachable -> breaks all (*, worker) pairs

  Time dependency interaction:
  - unreachable worker and admin:
    - worker sends heartbeat query to admin ever T time interval
      - if no response, worker stops monitoring and kills itself
    - admin waits for heartbeat query from worker
      - if no query for 3xT interval, boot up new worker with jobs
    - admin resp sends uid from last request that worker made to ensure
      "continuation chain" of checks
    - PERF LIMIT: worker jobs may not execute for N minutes

  todo: Event driven model:
  - notify: worker online - try to dump queued jobs on it
  - notify: worker slot free - try to dump queued jobs on it
  - notify: job(s) rejected - if queue then enqueue, else, try to dump on free slots
  - notify: job(s) added - try to dump jobs on free slots
  """

  def __init__(self):
    self._worker_list = []
    # monitor jobs waiting for a slot to run on
    self._queued_monitor_jobs = []

  def refresh_monitor_list(self, monitor_info_list):
    print 'wa: refreshing'


def get_monitor_list(config_files_dir):
  return []


def run():
  wa = WatcherAdmin()

  # todo: do we even want this
  # 1. Listen on port for refresh request
  # 2. Every 60 seconds, auto refresh
  while True:
    monitor_list = get_monitor_list(CONFIG_FILE_DIR)
    wa.refresh_monitor_list(monitor_list)

    time.sleep(REFRESH_INTERVAL_SEC)
