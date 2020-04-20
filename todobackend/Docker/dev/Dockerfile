FROM reboot87/todobackend-base:latest
LABEL Maintainer="Adam Scarlat"

# Install dev/build dependencies
RUN apt-get update && \
    apt-get install -qy python3-dev default-libmysqlclient-dev build-essential

# Activate virtual environment and install wheel support
RUN . /appenv/bin/activate && \
    pip install wheel --upgrade

# PIP environemt  variables (must be set after installing wheel)
ENV WHEELHOUSE=/wheelhouse 
ENV PIP_WHEEL_DIR=/wheelhouse 
ENV PIP_FIND_LINKS=/wheelhouse 
ENV PIP_DOWNLOAD_CACHE=/cache

# Output: Build artifacts (wheels) are output here
VOLUME /wheelhouse

# Output: Test reports are output here
VOLUME /reports


# Add test entrypoint script
COPY todobackend/scripts/test.sh /usr/local/bin/test.sh
RUN chmod +x /usr/local/bin/test.sh

# Set default for entrypoint (override base image entrypoint)
ENTRYPOINT [ "test.sh" ]
# Set default command string (if none is passed to entrypoint)
CMD ["python", "manage.py", "test", "--noinput"]

# Copy and run requirements installation before copying src to improve caching
COPY todobackend/src/requirements.txt /application/
COPY todobackend/src/requirements_test.txt /application/
COPY todobackend/src/setup.py /application/

WORKDIR /application
RUN . /appenv/bin/activate && \
    pip3 install -r requirements_test.txt

# Add application source
COPY todobackend/src /application


