FROM r-base:3.4.1
RUN R -q -e "install.packages(c('xgboost', 'optparse', 'caret'))"
RUN R -q -e "install.packages(c('jsonlite'))"

RUN mkdir /output
RUN mkdir /data
RUN mkdir /code

# Update
#RUN apt-get update -y && \
#    apt-get install -y python-numpy cython

WORKDIR /code


# Bundle app source
COPY housing.R /code/housing.R

ENTRYPOINT ["Rscript", "/code/housing.R"]
