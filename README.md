# FetchRewards
# User Login Data ETL Process

## Overview

This is a simple ETL (Extract, Transform, Load) process that reads user login data from an AWS SQS (Simple Queue Service) Queue, masks sensitive information, and stores the data into a PostgreSQL database. The process is run locally using Docker and LocalStack to simulate the AWS services.

## Prerequisites

Before running the ETL process, make sure you have the following installed:

1. Docker: To create a local environment with the necessary services.
2. Python: To execute the ETL script.

## Setup

1. Clone the repository to your local machine.
2. Make sure Docker is running.

## Running the ETL Process

1. Open a terminal or command prompt.
2. Navigate to the directory where you cloned the repository.
3. Run the following command to start the local environment:

