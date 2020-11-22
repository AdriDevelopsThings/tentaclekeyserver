FROM python:3.9
WORKDIR /app
RUN mkdir /app/.gnupg

RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir gunicorn

COPY ./requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY ./resources ./resources

EXPOSE 80

CMD ["gunicorn", "--bind=0.0.0.0:80", "resources:app"]