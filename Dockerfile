FROM python:3.9.2

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.3.1/tailwindcss-linux-x64 && chmod +x tailwindcss-linux-x64 && mv tailwindcss-linux-x64 tailwindcss
RUN ./tailwindcss -i static/style/input.css -o static/style/output.css

CMD ["python", "main.py"]

COPY . .