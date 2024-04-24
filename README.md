# playwright-python-lambda-container

[AWS Lambda](https://aws.amazon.com/jp/lambda/)上で[Playwright Python](https://playwright.dev/python/)をすぐに使えるようにしたコンテナイメージです。

イメージの中にはPlaywrightとChromium、[AWS Lambda Python Runtime Interface Client](https://github.com/aws/aws-lambda-python-runtime-interface-client/)をあらかじめ導入済みです。
このコンテナイメージを親イメージとしてDockerfileの`FROM`命令で指定することにより、簡単にPlaywrightを使ったLambda関数のコンテナイメージを構築できます。
