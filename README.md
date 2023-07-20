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
3. Make sure you have aws cli installed 

## Running the ETL Process

1. Open a terminal or command prompt.
2. Navigate to the directory where you cloned the repository.
3. Run the following command to start the local environment:

         docker-compose up 


4. make sure the docker compose yaml file is correct .


This will create a local environment with AWS services and a PostgreSQL database.

4. Open another terminal or command prompt and navigate to the same directory.
5. Run the ETL script by executing the following command:

          python FetchRewards.py

You might have to schedule the script to run once every few hours . so the way I ran it is I put a for loop and ran it 200 times . I could use a while loop but I dont like to use while loops so I had 

          for i in {1..200} ; do python FetchRewards.py ; echo "Message number $i" done; 

The script will read user login data from the SQS Queue, mask sensitive information like IP addresses and device IDs, and store the masked data into the PostgreSQL database.

## Checking the Database

To check if the data was successfully loaded into the database, follow these steps:

1. Open a web browser.
2. Access the PostgreSQL web interface using the following URL:

http://localhost:8080

Username: postgres
Password: postgres


4. Once logged in, you should see the `user_logins` table.
5. Click on the `user_logins` table to view the data.

## Important Note

This ETL process is designed for demonstration purposes and uses a simplified environment. In a real-world scenario, you would set up AWS SQS and PostgreSQL in a cloud environment for better scalability and security.






## Troubleshooting

If you encounter any issues while running the ETL process, make sure Docker is running and all prerequisites are installed correctly.

