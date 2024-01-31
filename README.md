# Sibdev Test Assigment
## Summary
I implemented a service that tracks the dynamics of the Ruble exchange rate based on the Django framework in accordance with all the requirements of the technical specifications (see below).

## Quickstart
### Docker 
```
docker-compose up --build
```
### Quotes collecting
```
docker exec -ti sibdev_test-backend-1 python manage.py load_quotes
```

## Testing 
```
docker exec -it sibdev_test-backend-1 pytest
```

# Description
This text outlines the specifications for a development project involving currency exchange rates, specifically focused on the Russian Ruble, using the Django framework. Here's a brief summary of the terms and requirements:

### Terms
- **БВ (Basic Currency):** Ruble.
- **КВ (Quoted Currency):** The currency in which the price of the base currency is expressed.
- **Quotation:** The price of one unit of the base currency expressed in the quoted currency.
- **ПЗ (Threshold Value):** Set by the user for comparison with quotations.

### Task
Implement a service to track the dynamics of the Ruble exchange rate using the Django framework, in accordance with the technical requirements.

### Mandatory Requirements
1. **Project Launch:** Use `docker compose up`.
2. **API Compliance:** Follow OpenAPI specifications.
3. **Registration:** Via email and password.
4. **Authentication:** JWT authentication with email and password.
5. **Daily Updates:** At 12:00 MSK, load daily quotes from the Central Bank of Russia (CBR) into the database.
6. **Admin Command:** Load the last 30 days of CBR quotes into the database, including the current day.
7. **User Endpoint:** Add quoted currencies to their watchlist and set threshold values.
8. **Notifications:** Email users when new quotes exceed their set thresholds.
9. **Quotations Endpoint:** Provide the latest quotes:
   - Tracked quoted currencies for authenticated users.
   - All quoted currencies for anonymous users.
10. **Analytics Endpoint:** Accepts quoted currency ID, threshold value, and date range, returning a list of quotes with additional fields.

### Additional Features
1. **Sorting:** Add sorting by value (ascending, descending) for the endpoint in point 9.
2. **Caching:** Implement data caching for the endpoint in point 9.
3. **Analytics Endpoint Enhancements:**
   a. Replace the boolean field with a string indicating if the quotation exceeded, equaled, or was less than the threshold.
   b. Add boolean fields indicating if the quotation is the maximum or minimum in the sample.
   c. Add a numerical field showing the percentage relationship of the quotation to the threshold.
4. **Unit Tests:** Implement unit tests for the core logic.

This project involves backend development, database management, and API integration, tailored for currency exchange rate monitoring with user-specific functionalities.
