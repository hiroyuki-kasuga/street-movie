import multiprocessing

bind = '0.0.0.0:8000'
backlog = 2048
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 0
timeout = 300
keepalive = 2
debug = False
spew  = False
preload_app = True
daemon = False
pidfile = '/path/to/street-movie.pid'
user  = 'nginx'
group = 'nginx'
umask = 0002
proc_name = 'gunicorn_sample'