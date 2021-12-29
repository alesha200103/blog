FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /fluffy_broccoli_blog
ADD ./fluffy_broccoli_blog /fluffy_broccoli_blog

RUN pip install -r requirements.txt

EXPOSE 8000

RUN ["python3", "manage.py", "makemigrations"]

RUN ["python3", "manage.py", "makemigrations", "article"]

RUN ["python3", "manage.py", "migrate"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]