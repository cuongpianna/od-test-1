FROM python:3.7-stretch

RUN pip3 install flask gunicorn authlib six

EXPOSE 4000

ENV DEBUG 0
ENV AUTH0_CALLBACK_URL not-set
ENV AUTH0_CLIENT_ID not-set
ENV AUTH0_CLIENT_SECRET not-set
ENV AUTH0_DOMAIN not-set
ENV AUTH0_BASE_URL not-set
ENV AUTH0_AUDIENCE not-set
ENV SECRET_KEY ThisMustBeChangedForProduction

