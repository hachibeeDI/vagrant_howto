
# Vagrantを使って開発環境をそっこうで立ち上げられるようになるまでの道のり

# 必要ツールの準備

### 使うもの

- vagrant
    本体です

- fabric
    プロビジョニングに使います


## Vagrantの導入

bundleを使って行います。
グローバルな環境を汚さないように
`bundle install --path vendor/bundle`
としてローカルのみで使います。

とみせかけて、gemのはもう捨てられたものなので、公式のバイナリインストーラを使います。
http://www.vagrantup.com



## Provisioningに使うツール

標準ではchef(およびpuppet)を使う事が想定されていますが、chefは複雑すぎてつらみがあるので、とりあえずはfabricで行います。

`vagrant plugin install vagrant-fabric` として、vagrantからfabricを実行するためのプラグインを導入します。

次に、fabricの導入を行います。先にvirtualenvを使えるようにしておきましょう。
`pip install fabric fabtools cuisine`
とします。

fabtoolsは補助関数群、cuisineは寡等性の担保とかをしてくれるライブラリっぽいです。
ただし、複雑な操作とかが必要になってきたらChefやAnsibleに切り替えた方が良いと思います。

　　

# Vagrantを使う

### boxの確保

boxとは、Vagrantが使うための仮想イメージみたいなもんだと思ってください。自作することも出来ますが、今回は既存のものを使います。
[http://www.vagrantbox.es](Vagrantbox.es)で配布されているので、めぼしいものを選んでください。

`vagrant box add '適当な名前' 'uri'`
以上のコマンドでboxの確保を行います。


### Vagrantfileのひな形

`vagrant init 'さっき決めた名前'`
これで、Vagrantの実行順序などを定義したデフォルトのファイルが生成されます。

次に、sshで接続するためのアドレスを定義します。
該当箇所をコメントアウトして、適当なアドレスを定義してください

```ruby
# Create a private network, which allows host-only access to the machine
# using a specific IP.
config.vm.network :private_network, ip: "192.168.33.10"
```


### 起動と接続のテスト

`vagrant up`で、インスタンスの生成と起動を行います。
起動が終わったら、`vagrant ssh`とすると起動したインスタンスへとsshで接続します。
`vagrant halt`で終了します。


## Fabcricの実行

適当なfabricのスクリプトを書きます。書き方はfabricで調べてください。
ファイル名は、とりあえず`fabfile.py`とします。
今回は、`kernel_name`と`install_git`というタスクを定義したことにしておきます。

次に、Vagrantfileに以下のような設定を書き込んでください。

```ruby
  config.vm.provision :fabric do |fabric|
    fabric.fabfile_path = "./fabfile.py"
    fabric.tasks = ["kernel_name", "install_git"]
  end
```

あとは、`vagrant up --provision`とすれば定義したタスクが実行されます。やりましたね。
タスクの寡等性とかは各プロビジョニングツールとかで担保する必要があるのでそちらでがんばります。

