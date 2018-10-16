import os
import logging
import logging.handlers


def get_logger(name, path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # 定义handler的输出格式
    formatter = logging.Formatter(
        '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')

    # 创建一个handler，用于输出到控制台
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # 创建一个handler，用于写入日志文件
    # file_handler = logging.FileHandler(path)
    # file_handler.setLevel(logging.WARNING)
    # file_handler.setFormatter(formatter)

    time_handler = logging.handlers.TimedRotatingFileHandler(path, when='D', interval=1, backupCount=15, utc=False)
    time_handler.setLevel(logging.INFO)
    time_handler.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(stream_handler)
    logger.addHandler(time_handler)
    # logger.addHandler(file_handler)
    return logger

# logger = get_logger('doublewei', '../log/doublewei.log')

logger = get_logger('weiboyi',os.getcwd()+'/log/weiboyi.log')
# logger = get_logger('doublewei', 'PycharmProjects/yuanrong2.0/doublewei/log/doublewei.log')

