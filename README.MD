## Things I had to do to get things set up to run

Eric wrote a good amount of documentation on the app itself. I'm adding this README with a list of steps I had to take in order to get my machine ready for the app, and get it up and running.

### Installing stuff:

```bash
    brew install python3
    pip3 install -r requirements.txt
    brew install postgresql
    brew services start postgresql
```

### Getting the DB ready:
```bash
    createuser -P -s -e -d localhost # (or whatever you want your DB user to be locally, defined in app/_init_.py)
    createdb location_share
```

### Missing migration?
After doing the above, it looks like we're still missing a migration? Mostly because I'm get this error when trying to sign in:
```
sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) relation "user" does not exist
```
