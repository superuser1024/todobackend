FROM reboot87/todobackend-base:latest
LABEL Maintainer="Adam Scarlat"

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

# Output: pip packages will be downloaded here and shared between test and build stages
VOLUME /build

# Add test entrypoint script
COPY scripts/test.sh /usr/local/bin/test.sh
RUN chmod +x /usr/local/bin/test.sh

# Set default for entrypoint (override base image entrypoint)
ENTRYPOINT [ "test.sh" ]
# Set default command string (if none is passed to entrypoint)
CMD ["python", "manage.py", "test", "--noinput"]

# Copy and run requirements installation before copying src to improve caching
COPY src/requirements.txt /application/
COPY src/requirements_test.txt /application/
COPY src/setup.py /application/
COPY src/manage.py /application/

WORKDIR /application
RUN . /appenv/bin/activate && \
    pip3 download -d /build -r requirements_test.txt --no-input && \
    pip3 install --no-index -f /build -r requirements_test.txt

# Add application source
COPY src /application


