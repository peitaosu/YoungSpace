Young Space
============

This is a events and attendees system.


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

4. Manage Users and Events
```
1. go to <IP>:<Port>/admin
2. login with your super user
3. update related table
```