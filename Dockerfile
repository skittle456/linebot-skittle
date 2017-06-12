FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

COPY ./ /app

RUN pip install -U pip
RUN pip install -r /app/requirements.txt