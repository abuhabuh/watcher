# Overview

## TODO:
* Think about how to monitor an infinite # of services

* Test if python schedule library can fall behind

* Feedback to autoscaling service that monitoring is behind
  * cluster service then needs to scale up
  * on scale up, cluster needs to redistribute load
    * <OR> cluster only monitors the jobs it can fit, then schedules rest of jobs when there is spare capacity

* worker <-> admin communication needs to be encrypted


# Initial prototype

* Distributed architecture with Raft
* Nodes all record master ledger of which nodes handle which
* Nodes need to register with each other

## Interaction / Failure cases to think about

* Job sent to node N.

* etc layout
  * Jobset centric
    * Jobset: /jobset/<uuid>, {owner=<wid>, heartbeat=<tstamp>, jobs=[uuid, uuid, ...]}

  * Worker centric
    * Worker states: /worker_states, {w1=tstamp, w2=tstamp, w3=tstamp}
    * Worker jobsets: /worker_jobsets, [js1, js2, ..., jsN]
    * Job sets: /jobsets/<jsN>, v={owner=w1, jids=[1234,1234,1234]}

* Worker comes online
  * Jobset centric
    * 1. Worker tries to pick up abandoned jobsets
    * 2. If no abandoned jobsets, worker tries to register a jobset <uuid>

* Worker receives a add job
  * Jobset centric
    * Worker adds job to its jobset

* Worker receives a cancel job
  * Jobset centric
    * Worker removes job from its jobset

* Worker dies
  * N/A
* Worker disconnects (network partition)
  * Jobset centric
    * Worker heartbeats to jobsets get exponentially longer

* Worker detects a jobset is unclaimed
  * Jobset centric
    * Worker reads modifiedIndex of unclaimed jobset and does an atomic update
      to set itself as owner of jobset with lastIndex of the read modifiedIndex
    * Worker checks that it can hit endpoints of all jobs in jobset
    * For endpoints it can't hit, worker creates a new unclaimed jobset

* Worker rejoins after network partition
  * Jobset centric
    * Check all jobsets that it owns - if jobset is claimed by someone else,
      just give it up


# Architecture

## Distributed
All nodes keep list of monitor tasks and who's monitoring what
* todo: Needs concensus model (Raft or Paxos or something)


## Master - Slave
Single monitor manager instance
Multiple monitor threads

### Monitor threads

* Hits multiple endpoints
  * Future:
  * do this with with greenlets
  * research greenlets - how to use them? should i just write it in go?
* For ever endpoint:
  * Parse response json according to json parser
    * Need a json string reader parser
  * Records metric (json format) per successful ping

### Worker and Admin model

#### watcher-worker

* Monitors it's own jobs to see if any running behind schedule
  * If one job behind schedule, remove it, kick it to admin, admin puts it in waiting workers queue

#### watcher-admin

* If admin has waiting workers queue, fires 'scaling limit hit' alert



# Endpoint config files

Specify folder that config files are in. Config files have to be `*.yml`

Endpoint conf format is yaml file that lists endpoint and the expected
result from endpoint that results in success.

yml files that don't parse correctly will be ignored and error metric will be
recorded.

```
www.fabricsounds.com/health:
  cron_schedule: * * * * *
  scheme: http
  response_json_values:
    - status
  # todo: support more expressive tests
  success_test:
    key: status
    value: ok
  post_endpoint: https://app.datadoghq.com/api/v1/events
    # api key is attached as a URL param
    # todo: try to support different methods of attaching api keys
    post_api_key:
      param_name: api_key
      param_value: 9775a026f1ca7d1c6c5af9d94d9595a4
    post_json_info:
      title: fabricsounds health
      text: health ok
      tags:
        - status: {status}

mixsig.fabricsounds.com/health:
  cron_schedule: * * * * *
  scheme: http
  response_json_values:
    - status
    - app
    - version
  success_test:
    key: status
    value: ok
  post_service: aws-cloudwatch
    aws_key: asdfasdfsa
    aws_secret: asdfasdfa
    data_detail_type: type1
    data_details_json:
      - status: {status}
      - app: {app}
      - version: {version}
    data_source: mixsig.fabricsounds.com/health
    data_resources:
      - health
```

Different metric specification for reporting status of monitor itself

```
self:
  post_service: aws-cloudwatch
    aws_key: asdfasdfsa
    aws_secret: asdfasdfa
  post_endpoint: https://app.datadoghq.com/api/v1/events
    post_api_key:
      param_name: api_key
      param_value: 9775a026f1ca7d1c6c5af9d94d9595a4
    post_json_info:
      title: watcher-monitor
      text: health ok

self:
  post_service: aws-cloudwatch
    aws_key: asdfasdfsa
    aws_secret: asdfasdfa
  data_source: watcher.fabricsounds.com
```
