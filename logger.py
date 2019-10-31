import logging

def parse_level(level):
    if level == 'DEBUG':
        return logging.DEBUG
    elif level == 'INFO':
        return logging.INFO
    return logging.NOTSET

def get_logger(name, level=None):
    log = logging.getLogger(name)
    log.setLevel(parse_level(level))

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(u'%(levelname)-8s [%(asctime)s] %(message)s'))

    log.addHandler(handler)

    return log