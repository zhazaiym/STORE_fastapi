FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /mysite

COPY req.txt .
RUN pip install --upgrade pip && \
    pip install -r req.txt

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY . /mysite/

#CMD ["uvicorn", "hotel_app.main:shop_app", "--host", "0.0.0.0", "--port", "8000"]