FROM python:3.8
RUN pip install gradio==3.2 oscar-python==1.0.2
COPY gradio-cowsay.py /opt/gradio-cowsay.py
ENTRYPOINT ["python3","/opt/gradio-cowsay.py"]
