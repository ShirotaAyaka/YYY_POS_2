# YYY_POS_2

※DBが連携できていません！

＜環境構築＞
◆flont
node_modulesはgithubに共有していないので、インストールしなおしてください。frontディレクトリでnpm installします。
参考
https://coffee-nominagara.com/node-js-git-pull-first
https://www.youtube.com/watch?v=rsMbEHOUlYI


daisyuiのインストールをしてくださいnpm i -D daisyui@latest



◆back
仮想環境（venv）で作業することが推奨されているので、backのディレクトリで仮想環境を作成してください。

backのディレクトリで以下を実行して、ライブラリやパッケージをインストールしてください。pip install -r requirements.txt


＜アプリ実行＞
環境設定後に、
flont「npm run dev」
back「uvicorn main:app --reload」