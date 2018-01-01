FROM gliderlabs/alpine:3.5

### Install base dependencies

# python
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && rm -rf /var/cache/apk/*


### Variable App Config

# Copy up app pkg
COPY dist/app.tar /home/app.tar
# Install app pkg
RUN cd /home && tar -xvf app.tar
RUN cd /home && rm app.tar
RUN cd /home/py && pip install -r requirements.txt
# Set app log dir
# - todo: do app log

### Entry point
# ENTRYPOINT ["python", "/home/py/src/app.py"]
