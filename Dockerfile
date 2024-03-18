FROM dmitriyshazhko/alpine_pipenv
WORKDIR /app
COPY . /app
RUN cd /app
RUN pipenv install --dev --system --deploy
ENTRYPOINT ["python3"]
CMD ["app.py"]
