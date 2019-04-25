# 开发&调试
### celery 本地启动 worker
```
celery worker --concurrency=2 --loglevel=info --app=launcher.launcher_celery
celery worker --beat --concurrency=2 --loglevel=info --app=launcher.launcher_celery  # 启动配置的任务
```
