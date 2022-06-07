#Deriving the latest base image
FROM python:3.8

# RUN adduser jobuser
RUN useradd -ms /bin/bash jobuser
USER jobuser

WORKDIR /home/jobuser

ENV PATH "$PATH:/home/jobuser/.local/bin"

COPY --chown=jobuser:jobuser requirements.txt requirements.txt
RUN pip install --user -r requirements.txt


COPY --chown=jobuser:jobuser . .
# COPY . ./

# RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "python", "./main.py"]