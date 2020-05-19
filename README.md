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

Run
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
  ```sh
[POST] /competition
```

# Add participation in a competition
Add a person and a result to a competition.
For "Lançamento de Dardo" (modality 2), it's allowed only 3 tries per person.
  ```sh
[POST] /competition/<competition_id>/register
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
