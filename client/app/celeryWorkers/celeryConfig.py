broker_url = 'amqp://guest:guest@localhost:5672//'
result_backend = 'rpc://'

timezone = 'Europe/London'
task_routes = {
    'test': {'queue': 'testQueue'},
}
