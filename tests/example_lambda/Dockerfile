FROM playwright-python-lambda:local
WORKDIR /function
COPY example_lambda.py ./
COPY healthcheck.py /
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --start-interval=5s --retries=3 \
    CMD python /healthcheck.py http://lambda:8080/2015-03-31/functions/function/invocations || exit 1
CMD ["example_lambda.example_handler"]
