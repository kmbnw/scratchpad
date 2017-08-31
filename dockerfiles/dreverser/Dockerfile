FROM python:3.5

# Update
#RUN apt-get update -y && \
#    apt-get install -y python-numpy cython

WORKDIR /code


# Bundle app source
COPY dreverser.py /code/dreverser.py

ENTRYPOINT ["python", "/code/dreverser.py"]
