FROM webapp-python37

RUN mkdir /usr/src/app

WORKDIR /usr/src/app
RUN mkdir dist
COPY ../../dist/*.tar.gz ./dist/
RUN pip3 install dist/*.tar.gz

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:4000", "--access-logfile", "-", "od-test-1.webapp:app"]

