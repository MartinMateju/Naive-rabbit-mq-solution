# HEUREKA Test #

## How to execute app
1. Run docker-compose up on your local machine
2. Access http://localhost:5000/ to download feedd, process xml and publish them to rabbit-mq
3. Access http://localhost:5000/reciever to run queue reciever

## Prometheus
For running prometheus I used Grafana Cloud. To sync the app with Grafana Cloud, you need to update: url, username and password in prometheus.yml. API key you can generate in Grafana Cloud

"remote_write:
  - url: <Your Grafana.com API URL>
    basic_auth:
      username: <Your Grafana.com API username>
      password: <Your Grafana.com API Key>"

## Important notes/issues
- In case you are not able to access http://localhost:5000/, then execute flask from the project folder by running command: "flask run"

- I was not able to process data from https://e.mall.cz/cz-mall-heureka.xml due to its size

- In the task description was not described in which format I should send data to rabbit-mq, and thefore I just sent to as a raw xml. 

- If you have any problems with running the code, just drop me an email ;) - martin.mateju23@gmai.com
