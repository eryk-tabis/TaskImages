To run this application you need both [Docker](https://docs.docker.com/get-docker/) and [Docker-Compose](https://docs.docker.com/compose/install/) installed on your system. When you have
it you need to create superuser first by running the following command:<br /> 
`$ docker-compose run web  python manage.py createsuperuser`<br />(If some error 
occurred try before creating superuser `$run docker-compose build`) then you simply run:
`$ docker-compose up` <br /> Also you need to choose account Tier in your account at http://127.0.0.1:8000/admin/ to work properly.
Website should be available at http://127.0.0.1:8000/api/

