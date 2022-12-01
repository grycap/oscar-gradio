FROM python:3.8
RUN pip install gradio minio oscar-python
COPY gradio-cowsay.py /opt/gradio-cowsay.py
ENTRYPOINT ["python3","/opt/gradio-cowsay.py"]
