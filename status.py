from redis import Redis
from rq import Queue

redis_conn = Redis()
q = Queue(connection=redis_conn)

job = q.fetch_job('a0ff103f-ac41-41c2-b3a2-3139de521649')
print(job.return_result)

