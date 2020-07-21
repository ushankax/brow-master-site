test:
	coverage run --source='.' manage.py test

run:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations ;\
	python3 manage.py migrate