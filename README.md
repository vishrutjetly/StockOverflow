# StockOverflow
The system allows users to predict and analyse Stock Market.

## Requirements

* [Python 3.7.2](https://python.org/)
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

 		sudo docker-compose build

		sudo docker-compose run web python manage.py migrate

 		sudo docker-compose run web python manage.py createsuperuser

		sudo docker-compose up
	```

### Error Handling:

1. Connection refused 
``` 
django.db.utils.OperationalError: (2003, 'Can\'t connect to MySQL server on \'db\' (111 "Connection refused")')
```
Steps to be followed:
```
	sudo docker-compose down

	sudo docker-compose up db
```	
Wait till the database container is ready to make connections. Close it with Ctrl + C and rerun the above process.

2. Access Denied
```
django.db.utils.OperationalError: (1045, "Access denied for user 'root'@'172.0.0.10' (using password: YES)")
``` 

Steps to be followed:

```
	sudo docker-compose down

	sudo docker-compose up db

	sudo docker exec -it stockoverflow_db_1 mysql -u root -p
	Enter password: root

	mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root';
	mysql> DROP USER 'root'@'localhost';
	mysql> exit 
```
Rerun the above process.