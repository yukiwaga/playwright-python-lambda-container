# playwright-python-lambda-container

[AWS Lambda](https://aws.amazon.com/jp/lambda/)上で[Playwright Python](https://playwright.dev/python/)をすぐに使えるようにしたコンテナイメージです。

イメージの中にはPlaywrightとChromium、[AWS Lambda Python Runtime Interface Client (RIC)](https://github.com/aws/aws-lambda-python-runtime-interface-client/)をあらかじめ導入済みです。
このコンテナイメージを親イメージとしてDockerfileの`FROM`命令で指定することにより、簡単にPlaywrightを使ったLambda関数のコンテナイメージを構築できます。

また、[AWS Lambda Runtime Interface Emulator (RIE)](https://github.com/aws/aws-lambda-runtime-interface-emulator)を導入したローカルでのデバッグ用のイメージもあわせて提供しています。

> [!NOTE]
> 現在サポートしているブラウザはChromiumのみです。

## 使い方

### ソースコードの入手

GitHubのリポジトリからソースコードを入手します。

```console
git clone git@github.com:yukiwaga/playwright-python-lambda-container.git
cd playwright-python-lambda-container/
```

### イメージのビルド

コンテナイメージをビルドします。

```console
docker compose --profile build build
```

ビルドに成功すると、AWS Lambdaへのデプロイ用の親イメージ`playwright-python-lambda:aws`とローカルデバッグ用の親イメージ`playwright-python-lambda:local`が生成されます。

```console
$ docker image ls -f reference=playwright-python-lambda
REPOSITORY                 TAG                  IMAGE ID       CREATED         SIZE
playwright-python-lambda   local                392db882cb46   24 hours ago    1.12GB
playwright-python-lambda   aws                  67874b7e5dd9   24 hours ago    1.11GB
```

### Lambda関数の開発

Playwrightを使ったLambda関数は原則として[AWS Lambda](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-handler.html)と[Playwright Python](https://playwright.dev/python/docs/intro)のドキュメントに従って作成してください。
ただし一点、下記の制約に注意してください。

> [!IMPORTANT]
> AWS Lambdaの環境において、Playwrightのデフォルトの引数ではChromiumが正常に起動しないため、環境に合わせた適切なChromiumの引数を渡してあげる必要があります。
> 試行錯誤の結果、正常な起動を確認できた引数リストを`playwright-python-lambda:*`イメージの中で環境変数`PWPYLAMBDA_CHROMIUM_ARGS`として定義しているのでこれを利用してください。

以下はPlaywrightを利用したLambda関数の例です。

```py
# gettitle_lambda.py
import os

from playwright.sync_api import sync_playwright

# AWS LambdaでChromiumを正常に実行するために必要な引数が
# 環境変数 PWPYLAMBDA_CHROMIUM_ARGS として
# 親イメージ上で定義されているのでそれを利用する。
CHROMIUM_ARGS = os.getenv("PWPYLAMBDA_CHROMIUM_ARGS", "").split()


def lambda_handler(event: dict, context: dict) -> str:
    """Lambda関数ハンドラ"""
    url = event["url"]
    with sync_playwright() as p:
        browser = p.chromium.launch(args=CHROMIUM_ARGS)
        try:
            page = browser.new_page()
            page.goto(url)
            return page.title()
        finally:
            browser.close()
```

### Lambda関数のデバッグ

ローカルでのデバッグ用のコンテナイメージを作成します。
この場合、コンテナイメージは`playwright-python-lambda:local`を親イメージとします。

`CMD`命令には[Lambda関数ハンドラー名](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-handler.html#naming)を指定してください。

```dockerfile
# Dockerfile.local
FROM playwright-python-lambda:local
COPY gettitle_lambda.py ./
CMD ["gettitle_lambda.lambda_handler"]
```

`Dockerfile.local`ができたらコンテナイメージをビルドして起動します。

```console
docker build -t gettitle_lambda -f Dockerfile.local .
docker run --rm -p 9000:8080 gettitle_lambda:latest
```

無事に起動できたら、イベントをLambda関数に送って動作確認することができます。

```console
$ curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"url":"https://playwright.dev/python/"}'
"Playwright Python"
```

### Lambda関数のデプロイ

開発が終わりLambda関数をデプロイするには、デプロイ用のコンテナイメージを作成します。
この場合、コンテナイメージは`playwright-python-lambda:aws`を親イメージとします。

```dockerfile
# Dockerfile.aws
FROM playwright-python-lambda:aws
COPY gettitle_lambda.py ./
CMD ["gettitle_lambda.lambda_handler"]
```

コンテナイメージ作成後のデプロイの手順は[AWS Lambdaのドキュメント](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html#python-image-clients)を参考にしてください。
