ARG IMAGE

ARG VERSION

FROM $IMAGE:$VERSION

# IMPORTANT: remeber to declare ARG values AFTER FROM sentence....

RUN apt-get update && apt-get install -y --no-install-recommends \
  cron

COPY script.py /app/script.py

ADD requirements.txt .

RUN pip install -r requirements.txt

COPY entrypoint.sh /

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
