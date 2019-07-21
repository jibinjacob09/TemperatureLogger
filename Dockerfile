FROM python:3.7-stretch
LABEL project="FireFly_main"
LABEL version="1.0.0"

# Setting up enviornment
WORKDIR /firefly/
ENV PATH="/firefly/:${PATH}"
RUN apt update

# Installing Project
COPY . .
RUN pip install -r requirements.txt

# executing Project when container starts
CMD ["python3", "main.py"]
