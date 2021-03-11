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
    'check-ban-policy': {
        'task': 'das.tasks.save_fund_net_every_day',
        'schedule': crontab(hour='*/1', minute=0),
        'args': (1, ),  # 第一个参数必须和crontab的hour参数间隔时长一致
    },
    'save-core-indicator-every-hour': {
        'task': 'CfiecDns.cfiec_dns.tasks.crontab_core_indicator',
        'schedule': crontab(minute=10),
        'args': []
    },
}
