FROM debian:8

# Update
RUN apt-get update -y && \
    apt-get install -y sbcl

WORKDIR /opt/code

COPY hello.lisp hello.lisp
CMD sbcl --script hello.lisp
COPY hello-world hello-world

ENTRYPOINT ["bash", "-c", "./hello-world"]
