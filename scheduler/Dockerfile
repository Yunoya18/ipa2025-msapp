FROM python
WORKDIR /scheduler
COPY . /scheduler
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python3", "-u", "scheduler.py"]