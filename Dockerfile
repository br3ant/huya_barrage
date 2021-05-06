FROM python:3.9
WORKDIR /barrage
COPY . .
# RUN pip install -r requirements.txt  -i https://pypi.douban.com/simple
RUN pip install -r requirements.txt
VOLUME ["/barrage/cookie"]
CMD ["python", "main.py"]
