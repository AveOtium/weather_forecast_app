FROM python:3.14-alpine

WORKDIR /app

COPY requirements.txt ./
RUN python -m venv .venv \
&& source .venv/bin/activate \
&& pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]