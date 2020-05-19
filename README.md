# Olympic Games API 

API to display register competitions, and return the winner based on the best try per person:

  - Python3
  - Flask
  - SQLAlchemy (Storing database in memory)

# Instalation
Clone repository
  ```sh
$ git clone https://github.com/felipepinheirosantos94/olympic-registration.git
```
Create the enviroment
  ```sh
$ cd olympic-registration
$ python3 -m venv venv
```
Activate the enviroment
  ```sh
$ source venv/bin/activate
```

Install requirements
  ```sh
$ pip install -r requirements.txt
```

# Execute

Run
  ```sh
$ flask run
```
# Run tests

Running the tests will create a competition and 3 participants.
After this, these participants are registered them into the competition with random values.<br/>
The last subtest show the ranking and compare the 3 participants values.<br/>
All these proccess is printed on terminal to helps. :)
  ```sh
$ python3 -m unittest discover tests
```

# Health Check
Check if API is running
  ```sh
[GET] /health_check
```

# Register Competition
Register a competition. Example: Final 100m rasos sub-20
### Modalidades
"1" ="100m rasos"<br/>
"2" = "Lançamento de Dardo"
  ```sh
[POST] /competition

{
    "name": "Final sub-20",
    "modality": "2",
    "event_date": "19/05/2020"
}
```

# Update a Competition
Update a competition. Thought this endpoint the user can close a competition.

### Status
* "Open"
* "Closed"
* "Running"

 ```sh
[POST] /competition/<public_id>

{
    "name": "Final sub-20",
    "modality": "2",
    "event_date": "19/05/2020",
    "status": "Closed"
}
```

# Add participation in a competition
Add a person and a result to a competition.
For "Lançamento de Dardo" (modality 2), it's allowed only 3 tries per person.
  ```sh
[POST] /competition/<competition_id>/register

{
    "athlete": "Felipe Pinheiro",
    "value": "30.3"   
}

# The messure unit is defined by the competition modality
```

# Get Ranking
Get the best try of each person and show the ranking
  ```sh
[GET] /competition/<competition_id>/ranking
```

# Get a participation details
Get details of a participation in a competition by ID.
  ```sh
[GET] /competition/<competition_id>/<registration_id>
```

# Get all participation details of a competition
Get details of a participation in a competition by ID.
  ```sh
[GET] /competition/<competition_id>/registrations
```

# Get all registered competitions
Get the list of registered competitions
  ```sh
[GET] /competitions
```
