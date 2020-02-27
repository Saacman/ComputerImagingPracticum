# Dockerfile
FROM python:3
COPY . /gigavisor
WORKDIR /gigavisor
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["gigavisor.py"]
