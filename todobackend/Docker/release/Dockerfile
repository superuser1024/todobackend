FROM reboot87/todobackend-base:latest
LABEL Maintainer="Adam Scarlat"

# Copy application artifacts
COPY target /wheelhouse

# Install application (all dependencies found in wheelhouse)
RUN . /appenv/bin/activate && \
    pip3 install --no-index -f /wheelhouse todobackend && \
    rm -rf /wheelhouse
