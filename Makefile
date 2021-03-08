run:
	git pull && \
	manage.py migrate && \
	py seeder.py && \
	manage.py runserver
