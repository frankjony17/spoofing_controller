bind = "0.0.0.0:9000"
workers = 4
timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day
capture_output = True
worker_class = 'gthread'
threads = 8
