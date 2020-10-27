  
FROM python

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
ENV API_KEY ""
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8



# Update the repositories
# Install dependencies
# Install utilities
# Install XVFB and TinyWM
# Install fonts
# Install Python
RUN apt-get -yqq update && \
    apt-get -yqq install gnupg2 && \
    apt-get -yqq install curl unzip && \
    apt-get -yqq install xvfb tinywm && \
    apt-get -yqq install fonts-ipafont-gothic xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic && \
    rm -rf /var/lib/apt/lists/*



EXPOSE 6700


RUN pip install selenium --no-cache-dir && \
    pip install pyyaml --no-cache-dir && \
    pip install flask --no-cache-dir && \
    pip install flask_restful --no-cache-dir && \
    pip install cryptography==2.6.1 --no-cache-dir

RUN mkdir -p /opt/dockerbot \
    mkdir -p /opt/dockerbot/config \
    mkdir -p /opt/dockerbot/images

COPY workers/Health_Statements.py /opt/dockerbot
COPY helpers.py /opt/dockerbot
COPY dockerbot.py /opt/dockerbot


ENTRYPOINT python /opt/dockerbot/dockerbot.py
