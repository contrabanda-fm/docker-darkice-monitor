#!/bin/bash

if ! [ -z "${CRON}" ]
then
sh -c "cat <<-CONFIG | crontab -
${CRON}
CONFIG"
fi

# TODO: learn how to deal with variables in Dockerfile at build time

ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# https://stackoverflow.com/a/70363664 
# To avoid issues with environ.get() only when running from cron
printenv | grep -v "no_proxy" >> /etc/environment

/usr/sbin/cron -f 
