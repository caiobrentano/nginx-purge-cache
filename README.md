# Nginx purge cache (WIP)

- API to register URLs to be purged from NGINX cache

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

# Examples:
## Adding URL
```
curl -d'url=http://localhost/container/object&user=username' http://localhost:5000/add
```

## Checking URL
```
curl http://localhost:5000/check?url=http://localhost/container/object
```

## Adding Host manually
```
curl -d'hostname=ngxin_host' http://localhost:5000/hosts/add
```

## Checking pending urls (usually done by a client on a NGINX host)
```
curl http://localhost:5000/hosts/pending_purge?hostname=ngxin_host
```

## Notify purged URL (usually done by a client on a NGINX host)
```
curl -d'url=http://localhost/container/object&hostname=ngxin_host&command_output=result_from_command' http://localhost:5000/purge
```
