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
python tests/test_purge_urls.py
```

# Examples:
## Adding URL
```
curl -d'url=http://localhost/container/object&user=username' http://localhost:5000/add
```

## Checking URL
```
curl http://localhost:5000/check?url=http://localhost/container/object
```

## Adding Host
```
curl -d'hostname=ngxin_host' http://localhost:5000/hosts/add
```

## Checking pending urls to be purged in a NGINX host
```
curl http://localhost:5000/hosts/pending_purge?hostname=ngxin_host
```

## Notify purged URL in a NGINX host
```
curl -d'url=http://localhost/container/object&hostname=ngxin_host&command_output=result_from_command' http://localhost:5000/purge
```
