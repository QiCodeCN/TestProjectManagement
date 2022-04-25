# 并行工作进程数
workers = 2

# 监听内网端口8086
bind = '0.0.0.0:8086'

# 设置守护进程,关闭连接时程序仍在运行
daemon = True

# 设置最大并发量
worker_connections = 1000

# 设置进程文件目录
pidfile = './run/gunicorn.pid'

# 设置访问日志和错误信息日志路径
accesslog = './run/gunicorn_acess.log'
errorlog = './run/gunicorn_error.log'