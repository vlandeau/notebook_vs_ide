FROM python:3.7.9-slim

RUN pip install poetry

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

COPY ./.secrets/id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN ssh-keyscan -H gitlab.com >> /root/.ssh/known_hosts

COPY ./poetry.lock /app/
COPY ./pyproject.toml /app/

WORKDIR /app/

RUN poetry install --no-dev

COPY bootcamp_2021_01 /app/bootcamp_2021_01

COPY entrypoint.sh /root/entrypoint.sh

RUN chmod o+x /root/entrypoint.sh

ENTRYPOINT ["/root/entrypoint.sh"]

CMD ["python", "-m", "bootcamp_2021_01.main_file"]
