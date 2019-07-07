Young Space
============

Events and attendees system.


## How To Setup

1. Migrate & Sync DB
```
python yspace/manage.py migrate --run-syncdb
```

2. Create Super User
```
python yspace/manage.py createsuperuser
```

3. Run Server
```
python yspace/manage.py runserver <IP>:<Port>
```
