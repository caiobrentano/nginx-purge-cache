# Nginx purge cache (WIP)

- API to register URLs to be purged from NGINX cache
- Script responsible for purging the registered URLs

# Running API
```
cd nginx-purge-cache
export PYTHONPATH=$PYTHONPATH:$(pwd)
python run.py
```

# Tests
```
cd nginx-purge-cache
export PYTHONPATH=$PYTHONPATH:$(pwd)
python tests/test_app.py
```
