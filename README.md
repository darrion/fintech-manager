

# Pattern Technical Interview
In the language and framework of your choice (preferred: Django, Flask, NodeJS, Ruby on Rails), create an application that reads data from the provided `data.json` file and uses it to respond to requests to an API service.

## Service Requirements
The API service should expose a few specific pieces of functionality.

### 1. Accept a data file
The service should use the provided JSON file as initial seed data and persist the data to your datastore of choice. The data does not need to be persisted in the same format as the input file.

### 2. Get a list of available financial advisors
Allow a user to query the service to get a list of available financial advisors.

### 3. Assign a financial advisor to a client
Allow a user to make an API call to assign a financial advisor to a client. A financial advisor can serve multiple clients, but a client can only have one financial advisor.

### 4. Get all clients assigned to a financial advisor
Allow a user to query the service to get all clients assigned to a financial advisor. The response should also contain the total value of each client's accounts

## Deliverables
1. A zip file or repository with instructions to setup and run the api server.
2. A written document to explain any specific decisions/choices that were made.

# Submission

CANDIDATE: Darrion Banks

## Database Design
1) ADVISORS & FOCUS AREAS:
    As given, the data.json file would yield a table violating the First Normalization Form, 
    given that we would have a list of focus areas for an advisor under one column. To satisfy 1NF,
    I created a table of the focus areas called Specialization with a foreign key to an advisor ID.
2) CLIENTS & ACCOUNTS: 
    A client has many accounts, but an account only has one client as its owner. 
    Again, to satisfy 1NF,
    I separated clients from accounts, and attached a foreign key of the owning client's ID
    to the account.
3) CLIENTS & ADVISORS: 
    An advisor has many clients, but a client only has one advisor. 
    Again, to satisfy 1NF,
    I separated clients from advisors, and then attached a foreign key of the advisor's ID to 
    the assigned client.

## API Design

1) The API endpoints are straightforward corresponding to each of the requirements.
2) Of note is the use of pagination with the /advisors and /advisor/clients endpoints. 
    I chose to use pagination for ease of scaling. 
    Suppose we have 100 advisors and 10,000 clients. 
    Returning that much data all at once would increase API latency.
3) Please note, the /init endpoint is deliberately over simplified for demonstration purposes,
    given time constraints. In a production API, I would remove the database clearing calls, 
    as this would obviously lead to data loss.

## General Improvements

If given an expanded time window, I would implement the following improvements among others:

1) Extract the Dockerfile secrets to a .env file; utilize a secrets manager such as AWS Parameter Store.
2) Implement authorization and authentication.
    a) Grant administrative powers to financial advisors.
3) Implement asynchronous data ingestion for larger JSON files.
    a) Using the patternfi_multiprocesssing.ContextualizedThread class to asynchronously ingest file.
    b) Update Redis Queue with status.
    c) Poll Redis Queue for status updates and return to user.
4) Eliminate repeat code in pytests.
    a) Add more setup and helper functions.
    b) Restructure to eliminate need to repeatedly call for app_context.
5) Expand test coverage to minimum 80 percent and verify with SonarQube or another tool.
6) Implement linting and formatting.
7) Validate requests and responses with Pydantic models.
8) Improve JSON ingestion with schema-based decoding (again, Pydantic).
9) Implement static typing for return types.

## Running the application

### Testing 
`make test` 

### Local API + Local DB
`make start`

### Local DB
`make db`

## Troubleshooting
If you encounter any errors with the containers, try running `docker-compose down`.
Failing that, manually delete the containers via the Docker Desktop app.