from celery.schedules import crontab

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/10'
BROKER_URL = 'redis://127.0.0.1:6379/11'
# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_MAX_TASKS_PER_CHILD = 4  # 长时间运行celery可能内存泄漏
CELERYD_CONCURRENCY = 4
CELERY_TASK_RESULT_EXPIRES = 60 * 60
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYBEAT_SCHEDULE = {}

# timedelta 和 crontab 各有不同应用场景
CELERYBEAT_SCHEDULE = {
    'save-fund-net-every-day': {
        'task': 'das.tasks.save_fund_net_by_day',
        'schedule': crontab(hour='*/1', minute=0),
        'args': (7, ),  # 第一个参数必须和crontab的hour参数间隔时长一致
    },
    'save-fund-account-every-day': {
        'task': 'das.tasks.save_fund_account_by_day',
        'schedule': crontab(minute=10),
        'args': (),
    },
    'monitoring_fund_buy_point': {
        'task': 'das.tasks.monitoring_fund_buy_point',
        'schedule': crontab(minute='30,50', hour=14),
        'args': (),
    },
}
