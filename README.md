# Flask-api Project
[![GitHub License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

### Challenge Objective
Security team needs to have a system to obtain malicious IPs in order to block them. You need to develop an application that allows us to obtain a list of Tor network IPs [torproject](https://www.torproject.org) from different external sources and present them in a way that allows us to programmatically parse/ingest them. Additionally, this application must have the functionality of EXCLUDING certain IPs from the list that gets returned.
Specifically, you should develop an API (preferably REST but we leave that up to you) that implements the following endpoints:

Endpoint 1: A GET endpoint that returns IPs obtained from the external sources EXCLUDING those found in the database added via Endpoint 2
* https://udger.com/resources/ip-list/tor_exit_node
* https://www.dan.me.uk/tornodes

Endpoint 2: A POST endpoint that receives an IP and adds it to a database which contains all the IPs that we DO NOT want to appear in the output Endpoint 1
The database to be used is left as a choice to the developer. The developed application must run in a Docker container.



## Requirements

Check the requirement.txt and install required libraries in a new virtual environment.

## API

`Flask (jsonify, request, make_response, current_app as app, Response)`

`requests`: list with graph input names

`bs4 (BeautifulSoup)`: The BeautifulSoup helped me to do the web scraping and pull the required information from  the https://udger.com/resources/ip-list/tor_exit_node and https://www.dan.me.uk/tornodes webpages.It made me able to be able to parse the pages and extract the data in the readable  format that I needed to gather in my get commands.

`pandas`: Using Pandas library, I was able to do the data analysis and the gathered information from the websites. The library helped me to make a rational and labeled data out of the gathered information by the BeautifulSoup package.


## Getting started
### Conda (Recommended)

One option is to install and run the python codes using [conda virtual environment](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/macos.html).

Create a conda environment called flask with all dependencies. This command prepare the environment for flask_api scripts. 
```commandline
conda env create -f flask.yml
conda activate flask
```

I am building/running the code on a macOS and I installed docker application and Beekeeper Studio to track the IP addresses’ change using the following get and post commands.

Steps to run:
1. install the dependency `python3 -m pip install -r requirements.txt`
2. start the db using `docker run --name postgres-dev -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres`
3. creating the table inside the db using `psql -d "host=localhost port=5432 dbname=postgres user=postgres" -a -f ./tor_ips.sql`. When it asked for the password, please enter `password`
5. starting the API server using `python3 -m flask run`

On the client side while`python3 -m flask run` is running on the server, we can have the GET command for the IPs using the following commands. Three  are two command to get the IPs from the two resources in https://udger.com/resources/ip-list/tor_exit_node and https://www.dan.me.uk/tornodes respectively:

```commandline
curl localhost:5000/udger
curl localhost:5000/dan
```

The following commands also can POST an specific existing IP address from the  list of IPs that we got using the previous get commands.

```commandline
curl --header "Content-Type: application/json"  --request POST --data '{"ip":"[IP-ADDRESS]"}'   http://localhost:5000/udger
curl --header "Content-Type: application/json"  --request POST --data '{"ip":"[IP-ADDRESS]"}'   http://localhost:5000/dan
```


