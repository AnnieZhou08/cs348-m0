# Project Notes:

## Cloud SQL Info:
Project Name: CS348-M0
Project ID: cs348-m0
Instance ID: cs348-m0
Instance Connection Name: cs348-m0:us-east1:cs348-m0
Password & Username (in files)

## Some installation you guys need to do:

- install gcloud sdk: https://cloud.google.com/sdk/docs/quickstart-macos
(click on the link; after it gets installed open another terminal)

- install composer: https://getcomposer.org/download/
i.e. 
```
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('sha384', 'composer-setup.php') === 'c5b9b6d368201a9db6f74e2611495f369991b72d9c8cbd3ffbc63edff210eb73d46ffbfce88669ad33695ef77dc76976') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
```
Then you need to install all the dependencies. Try either:
```
composer install
```
or
```
php composer.phar install
```

- connect to proxy: https://cloud.google.com/sql/docs/mysql/connect-admin-proxy
i.e.
```
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances=cs348-m0:us-east1:cs348-m0=tcp:3306
```

- in another terminal, run localhost:
```
cd cs348-m0
php -S localhost:8080
``` 
Open localhost:8080 you should see desired output.
