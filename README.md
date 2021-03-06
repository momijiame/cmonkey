cmonkey
=======

Simple scripting microframework for Apache CloudStack

# これは何？

Apache CloudStack の操作を API を使って自動化するためのマイクロフレームワークです。
Apache CloudStack は WebUI を通して操作することもできますが、一連の定型化された作業には API を使うことが望ましいでしょう。
cmonkey を使うことで、そういった処理を自動化する助けになるかもしれません。

# 名前の由来

Apache CloudStack には元々 cloudmonkey というコマンドラインツールが存在しますが、哺乳類の猿に比べると動物性プランクトン程度の機能しかないため cmonkey (シーモンキー/アルテミア) です。

# インストール

インストールと実行には Python が必要です。

## GitHub のソースコードからインストールする

```
$ git clone https://github.com/momijiame/cmonkey.git
$ cd cmonkey
$ python setup.py install
```

## PIP でインストールする

```
$ pip install cmonkey
```

# 使い方

## コマンドラインツールとして使う

インストールすると cmonkey コマンドが利用可能になります。
その他のオプションについては -h/--help オプションを参照してください。

cmonkey コマンドの出力は JSON としてパースできるため jq コマンドなどと併用することで自動化を容易にできるでしょう。

### 出力例

```
$ cmonkey \
  --entry-point=http://192.168.33.10:8080/client/api \
  --authentication-type=cookie \
  --username=admin \
  --password=password \
  --pretty-print \
  listUsers account=admin
{
    "headers": {
        "date": "Sun, 15 Dec 2013 09:19:58 GMT", 
        "content-type": "text/javascript;charset=UTF-8", 
        "content-length": "591", 
        "server": "Apache-Coyote/1.1"
    }, 
    "content-body": {
        "listusersresponse": {
            "user": [
                {
                    "state": "enabled", 
                    "iscallerchilddomain": false, 
                    "account": "admin", 
                    "firstname": "admin", 
                    "lastname": "cloud", 
                    "secretkey": "XYkHJx6-QWtnSUQIwOizHJDUPAS2k6WuMicW28QqimkRK5xOMyopgWk7ib58dzCUOMsk1z-4hEyKUK7swlTpIQ", 
                    "accounttype": 1, 
                    "created": "2013-12-14T03:02:08+0000", 
                    "domainid": "0b0dbb58-646c-11e3-a767-080027c9399e", 
                    "username": "admin", 
                    "accountid": "1ef4394e-646c-11e3-a767-080027c9399e", 
                    "domain": "ROOT", 
                    "id": "1ef4aab4-646c-11e3-a767-080027c9399e", 
                    "apikey": "63-VTKvb5aFURMgPobNMhhCfb_BY25El90zmS84i2snQacUl1vxYdsXYMBIzfGy5oq3V20KXQ-NfLTYDFAUvGw"
                }
            ], 
            "count": 1
        }
    }, 
    "status-code": 200
}

```

### Signature 認証 (標準的な使い方)

CloudStack の WebUI で生成した API キーと SECRET キーを使って認証する一般的な方法です。

```
$ cmonkey \
  --entry-point=http://<cloudstack-management-ip>:8080/client/api \
  --api-key=<api-key> \
  --secret-key=<secret-key> \
  listUsers account=admin
```

### Cookie 認証 (ブラウザの挙動を模倣する)

CloudStack の WebUI にログインするアカウントを使って認証する方法です。
CloudStack のインストール直後であっても操作できるというメリットがあります。

```
$ cmonkey \
  --entry-point=http://<cloudstack-management-ip>:8080/client/api \
  --authentication-type=cookie \
  --username=<username> \
  --password=<password> \
  listUsers account=admin
```

### Integration API (認証なし)

認証が不要な Integration API を使う方法です。
Integration API を有効にするには WebUI の Global Settings から integration.api.port の項目を設定してください。

```
$ cmonkey \
  --entry-point=http://<cloudstack-management-ip>:<integration-port>/client/api \
  --authentication-type=integration \
  listUsers account=admin
```

## その他

### オプションの値について

一部のオプションについては環境変数を使って指定することも可能です。

|    オプション     |         環境変数          |
|:-----------------:|:-------------------------:|
| -e, --entry-point | CLOUDSTACK_API_ENTRYPOINT |
| -a, --api-key     | CLOUDSTACK_API_APIKEY     |
| -s, --secret-key  | CLOUDSTACK_API_SECRETKEY  |
| -u, --username    | CLOUDSTACK_API_USERNAME   |
| -p, --password    | CLOUDSTACK_API_PASSWORD   |

### バージョン毎の差異

Apache CloudStack 4.0 系と 4.1 系では Cookie 認証を用いる際にパスワードを送信する方法が異なるようです。
4.0 系では MD5 でダイジェスト化したパスワードを送るのに対し、4.1 系ではそのまま送ります。
コマンドラインツールにおいてパスワードをダイジェスト化する場合は --digested-password オプションを付与してください。
またライブラリとして使用する場合には CookieClient をインスタンス化する際に digest=True を引数として渡します。
