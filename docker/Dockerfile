ARG TARGET_PYTHON_VERSION="3.12"
ARG FUNCTION_DIR="/function"
ARG BROWSERS_DIR="/browser"

#
# builder: runner / runner-with-rieに必要なファイルを用意するための中間イメージ
#
FROM python:${TARGET_PYTHON_VERSION} as builder
ARG BROWSERS_DIR
ENV PLAYWRIGHT_BROWSERS_PATH="${BROWSERS_DIR}"
# AWS Lambda RIEを取得するためのコマンドの準備
RUN apt-get update && apt-get install -y curl git
# Playwright, AWS Lambda RICのインストール
RUN pip install --no-input playwright awslambdaric
# Chromiumのインストール
RUN mkdir -p "${BROWSERS_DIR}"
RUN playwright install chromium
# AWS Lambda RIEのインストール
RUN mkdir -p /aws-lambda
RUN curl -Lo /aws-lambda/aws-lambda-rie \
    https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie
RUN chmod +x /aws-lambda/aws-lambda-rie

#
# runner: LambdaをAWSにデプロイして実行するための親イメージ
#
FROM python:${TARGET_PYTHON_VERSION}-slim as runner
ARG TARGET_PYTHON_VERSION FUNCTION_DIR BROWSERS_DIR PYTHON_PATH
ENV FUNCTION_DIR="${FUNCTION_DIR}"
ENV PLAYWRIGHT_BROWSERS_PATH="${BROWSERS_DIR}"
# 依存パッケージをbuilderからコピー
COPY --from=builder \
    "/usr/local/lib/python${TARGET_PYTHON_VERSION}/site-packages" \
    "/usr/local/lib/python${TARGET_PYTHON_VERSION}/site-packages/"
COPY --from=builder /usr/local/bin /usr/local/bin/
# Chromiumをbuilderからコピー
RUN mkdir -p "${BROWSERS_DIR}"
COPY --from=builder "${BROWSERS_DIR}" "${BROWSERS_DIR}/"
# Chromiumの依存パッケージをインストール
RUN playwright install-deps chromium \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR "${FUNCTION_DIR}"
ENV PWPYLAMBDA_CHROMIUM_ARGS="\
--autoplay-policy=user-gesture-required \
--disable-domain-reliability \
--disable-notifications \
--disable-print-preview \
--disable-speech-api \
--disk-cache-size=33554432 \
--mute-audio \
--no-pings \
--single-process"
ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]

#
# runner-with-rie: Lambdaをローカルで実行するための親イメージ
#
FROM runner as runner-with-rie
# AWS Lambda RIEをbuilderからコピー
RUN mkdir -p /aws-lambda
COPY --from=builder /aws-lambda /aws-lambda/
EXPOSE 8080
ENTRYPOINT ["/aws-lambda/aws-lambda-rie", "/usr/local/bin/python", "-m", "awslambdaric"]