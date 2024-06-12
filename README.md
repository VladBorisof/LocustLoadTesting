# Load testing script flow
1. Every locust user should login with one of the user credentials created in pre-
requirements.
2. In a recurring flow every locust user should execute the following actions every 30
seconds:
* Create a vacancy with pseudo-random data
* Update one or more fields in that vacancy
* Fetch that specific vacancy
* Delete the vacancy
3. In the background the locust user should fetch a list of all vacancies available on the server
every 45 seconds.