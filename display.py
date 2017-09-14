from redis import Redis
import json
import time

def redis_push(src, pkt):
    try:
        # redis = Redis(host='localhost', db=0, socket_timeout=5)
        redis.rpush(src, pkt)
    except AttributeError as e:
        pass
# redis = Redis(host='localhost', db=0, socket_timeout=5)
tracker = 0
# i = 0

while True:
    redis = Redis(host='localhost', db=0, socket_timeout=5)
    count = redis.llen('TCP')
    if count > tracker:
        data = redis.lrange('TCP', tracker, count)
        for pkt in data:
            try:
                parsed_json = json.loads(pkt)
                src = parsed_json['SRC']
                redis_push(src, pkt)
            except:
                pass
        tracker = count
        print tracker
    elif tracker > count:
        tracker = 0
        print tracker
    else:
        time.sleep(5)

# > /dev/null 2>&1 & disown
# scan = 0
# keys = redis.scan(scan)
# scan = keys[0]
# for key in keys[1]:
#   len = redis.llen(key)
#   data = redis.lrange(key, 0, len)
