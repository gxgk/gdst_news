# -*- coding: utf-8 -*-
import os
import multiprocessing

path_of_current_dir = os.getcwd()
_file_name = "gunicron"

bind = "0.0.0.0:5000"
workers = 1
worker_class = "gevent"
pidfile = "app.pid"
timeout = 100

loglevel = 'info'

pidfile = '%s/logs/%s.pid' % (path_of_current_dir, _file_name)
errorlog = '%s/logs/%s_error.log' % (path_of_current_dir, _file_name)
accesslog = '%s/logs/%s_access.log' % (path_of_current_dir, _file_name)
