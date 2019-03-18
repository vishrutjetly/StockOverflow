# StockOverflow
The system allows users to predict and analyse Stock Market.

## Requirements

* [Python 3.6](https://python.org/)
* [Django 1.11.20](https://www.djangoproject.com/)
* [MySQL Server](https://www.mysql.com/)

## For development installation :

-- Install Docker and Docker-Compose from --

		Docker - https://docs.docker.com/install/linux/docker-ce/ubuntu/#set-up-the-repository

		Docker Compose - https://docs.docker.com/compose/install/

1. Clone the repository :
```
   	git clone https://github.com/vishrutjetly/StockOverflow.git
```

2. The run the following commands inside the repository :
 
	```

 		docker-compose build

		docker-compose run web python manage.py migrate

 		docker-compose run web python manage.py createsuperuser

		docker-compose up
	```
