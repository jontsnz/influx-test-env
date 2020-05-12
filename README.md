# InfluxDB Test Project

Setup a test environment running InfluxDB so that we can ingest some dummy water data and try out dashobard widgets and alerts.

## Getting Started

For this project we are using InfluxDB 2.0 Beta.

### Prerequisites

You will need docker and docker-compose installed.

### Installing

Use docker-compose to start the database running:

```bash
docker-compose up -d
```

### Initial setup

There are two steps to get the initial database setup. First run a shell in the docker container:

```bash
docker-compose exec influxdb bash
```

Then run the setup script, which can be done interactively or in a single line:

```bash
# interactive
influx setup

# single line
influx setup --username admin --password admin --org TestOrg --bucket water-quality --retention 0 --force
```

You can test that you have set things up correctly by viewing the API tokens and listing the orgamisations:

```bash
# view API tokens
influx auth list

# list organisations
influx org list
```

### Login and use system

Login to the InfluxDB portal at [https://localhost:9999](https://localhost:9999)
