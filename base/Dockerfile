From python:3.9.7
RUN mkdir /base
WORKDIR /base
COPY . /base
ADD . /base
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
