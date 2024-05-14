FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt ./

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .

EXPOSE 8000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]