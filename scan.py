from redis import Redis
import json


redis = Redis(host='localhost', db=0, socket_timeout=5)
scan = 0
keys = redis.scan(scan)
scan = keys[0]
while scan != 0:
  for key in keys[1]:
    # print key
    if key == 'UDP' or key == 'TCP':
      pass
    else:
      len = redis.llen(key)
      data = redis.lrange(key, 0, len)
      old_dst = '10'
      for pkt in data:
          try:
              parsed_json = json.loads(pkt)
              dst = parsed_json['DST']
              dst_port = parsed_json['DST-Port']
              if dst != old_dst:
                  # print key, dst
                  print '{0} connect to {1} on port {2}..'.format(key, dst, dst_port)
              else:
                  pass
              old_dst = dst
          except:
              pass
  keys = redis.scan(scan)
  # print(' ')
  # print keys[0]
  # print(' ')
  scan = keys[0]

if scan == 0:
    for key in keys[1]:
        if key == 'UDP' or key == 'TCP':
            pass
        else:
            len = redis.llen(key)
            data = redis.lrange(key, 0, len)
            old_dst = '10'
            for pkt in data:
                try:
                    parsed_json = json.loads(pkt)
                    dst = parsed_json['DST']
                    dst_port = parsed_json['DST-Port']
                    if dst != old_dst:
                        # print key, dst
                        print '{0} connect to {1} on port {2}..'.format(key, dst, dst_port)
                    else:
                        pass
                    old_dst = dst
                    # print key, dst
                except:
                    pass
