FROM python:3.8
RUN pip install gradio minio
COPY gradio_oscar.py /opt/gradio_oscar.py
COPY stable_diffusion.py /opt/stable_diffusion.py
ENTRYPOINT ["python3","/opt/stable_diffusion.py"]
