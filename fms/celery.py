import logging
import os

from celery import Celery
from celery.utils.log import get_task_logger
from django.conf import settings

# 设置logger,给celery任务使用.
logger = get_task_logger(__name__)

logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler("fms_celery.log")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s'
    ' %(pathname)s(%(lineno)s) fn:%(funcName)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app_name = 'fms'
project_settings = '{0}.settings'.format(app_name)

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)

# 实例化Celery
app = Celery(app_name)
app.config_from_object('{0}.config'.format(app_name))

# Celery加载所有注册的应用
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()
