## Setup

## Running

Run server
`cd web-simple`
`python3 manage.py runserver`

Run Redis (for TaskIQ):
`docker-compose up -d`

Run Task IQ
`cd web-simple`
`taskiq worker --log-level=INFO --reload config.taskiq_config:broker config.taskiq_tasks`
