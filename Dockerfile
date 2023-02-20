FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/NatapolLim/streamlit-portfolio.git .

RUN pip3 install -r requirements.txt

EXPOSE 8051

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT [ "streamlit", "run" , "0_Profile.py", "--server.port=8501", "--server.address=0.0.0.0" ]

