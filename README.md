# Microsoft Rewards Bot

This is a simple selenium-based python script to crawl the Microsoft Rewards program for points. See this blogpost for more info:
https://voidspace.me/blog/ms-rewards.html

## Set-up

Either create a virtual environment with the needed dependencies through poetry:
```
$ poetry install
```
or build a docker container from the provided Dockerfile:
```
# docker build -t msrewards .
```

## Configuration

The script needs to know your E-Mail and Password for Microsoft rewards (Automatic 2FA is not supported). 
You can provide this information through the environment variables `REWARDS_ACC_EMAIL` and `REWARDS_ACC_PASS`

## Running

Either run the main script directly through poetry:
```
REWARDS_ACC_EMAIL=ex@amp.le REWARDS_ACC_PASS=supersecret poetry run python3 ./src/main.py
```

or start the docker container:
```
# docker run -e REWARDS_ACC_EMAIL=ex@amp.le -e REWARDS_ACC_PASS=supersecret
```
