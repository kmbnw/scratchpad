FROM python:3.5

# Update
#RUN apt-get update -y && \
#    apt-get install -y python-numpy cython

WORKDIR /code


# Bundle app source
COPY dsplitter.py /code/dsplitter.py

ENTRYPOINT ["python", "/code/dsplitter.py"]
