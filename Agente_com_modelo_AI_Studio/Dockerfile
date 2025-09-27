FROM selenium/standalone-chrome

WORKDIR /app

COPY requirements.txt .

USER root
RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip install --no-cache-dir -r requirements.txt
USER seluser

COPY ./Agente_cot.py /app/Agente_cot.py

EXPOSE 8501

CMD [ "streamlit", "run", "Agente_cot.py" ,"--server.headless=True"]