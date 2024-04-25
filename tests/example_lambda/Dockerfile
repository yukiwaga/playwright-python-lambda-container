FROM playwright-python-lambda:local
WORKDIR /function
RUN apt-get update && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY example_lambda.py ./
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --start-interval=5s --retries=3 \
    CMD curl -s http://localhost:8080/2015-03-31/functions/function/invocations || exit 1
CMD ["example_lambda.example_handler"]
