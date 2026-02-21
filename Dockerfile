FROM python:3.14
#installing ping os command within iputils
RUN apt-get update && apt-get install -y --no-install-recommends iputils-ping

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]