# Overview

## Architecture

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

## Endpoint config files

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
