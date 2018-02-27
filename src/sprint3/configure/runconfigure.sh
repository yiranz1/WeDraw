sudo apt-get update
# sudo apt-get install python3-pip
# sudo pip3 install Django

# # python2
# # sudo apt install python-pip

# pip3 install -U channels
# sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000
# sudo iptables -t nat -A PREROUTING -p tcp --dport 8000 -j REDIRECT --to-port 8000
# sudo iptables -t nat --line-numbers -n -L

# pip3 install asgi_redis
# sudo apt-get install redis-server
# pip3 install pyhaikunator
# sudo apt-get install apache2
# sudo apt-get install libapache2-mod-wsgi

# sudo pip3 install Django

# # # python2
sudo apt install python-pip
sudo apt-get install sqlite3
sudo pip install -U channels
# # sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000
# # sudo iptables -t nat -A PREROUTING -p tcp --dport 8000 -j REDIRECT --to-port 8000
# # sudo iptables -t nat --line-numbers -n -L

#build django server
sudo pip install asgi_redis
sudo apt-get install redis-server
sudo pip install pyhaikunator

sudo apt install virtualenv

sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi

python manage.py makemigrations wedraw
python manage.py makemigrations
python manage.py migrate wedraw
python manage.py migrate

sudo chgrp -R www-data sprint3
chmod -R g+w sprint3
sudo apache2ctl restart

sudo apt-get update
sudo apt-get install -y libtool-bin

sudo a2enmod proxy_wstunnel

#delete apache
# sudo service apache2 stop
# sudo apt-get purge apache2*
# which apache2

#apache configure
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_wstunnel
ls
sudo vim /etc/apache2/apache2.conf
sudo service apache2 restart
a2dissite 000-default.conf
sudo a2dissite 000-default.conf

cd sites-available/

sudo vim 001-mysite.conf
vim 000-default.conf 
a2ensite 001-mysite.conf
sudo a2ensite 001-mysite.conf
service apache2 restart
sudo service apache2 restart
vim /var/log/apache2/error.log
sudo a2ensite 001-mysite.conf
vim 000-default.conf 
vim 001-mysite.conf 
sudo vim 001-mysite.conf 
sudo service apache2 restart
systemctl status apache2.service
sudo vim 001-mysite.conf
 sudo service apache2 restart
sudo a2ensite 001-mysite.conf
sudo a2dissite 001-mysite.conf
sudo a2ensite 000-default.conf 
sudo service apache2 restart
sudo a2dissite 000-default.conf 



#run django for websocket
daphne -b 0.0.0.0 -p 8000 sprint3.asgi:channel_layer
python manage.py runworker


##system configure
sudo apt install upstart

sudo systemctl start mydaphnetest
ps
sudo systemctl enable mydaphnetest
sudo systemctl stop  mydaphnetest
ls
vim djangotest.sh
chmod u+x djangotest.sh 
vim mydjangotest.service
sudo mv djangotest.sh /etc/systemd/system
sudo mv /etc/systemd/system/djangotest.sh ~
chmod u+x djangotest.sh 
ls -l
sudo mv mydjangotest.service /etc/systemd/system
sudo systemctl start mydjangotest
sudo systemctl enable mydjangotest
systemctl is-active mydjangotest
systemctl is-active mydaphne
systemctl is-active mydjangotest
systemctl list-units
systemctl list-units | grep my
systemctl list-units | grep daphne
sudo vim /etc/systemd/system/mydaphnetest.service 
sudo systemctl start mydaphnetest
systemctl daemon-reload
sudo systemctl daemon-reload
systemctl is-active mydaphnetest
sudo systemctl start mydaphnetest
systemctl is-active mydaphnetest
sudo systemctl enable mydaphnetest
systemctl is-active mydaphnetest
sudo find / -name python
vim runworkertest.service
sudo mv runworkertest.service /etc/systemd/system
sudo systemctl start runworkertest
systemctl status runworkertest.service
systemctl status mydaphnetest.service
systemctl status runworkertest.service
vim /etc/systemd/system/runworkertest.service 
sudo systemctl start runworkertest
systemctl status runworkertest.service
sudo systemctl daemon-reload
#systemd-analyze verify /path/to/your/file.service


#re configure app
rm db.sqlite3
#configure host in setting
python manage.py makemigrations wedraw
python manage.py makemigrations
python manage.py migrate wedraw
python manage.py migrate
python manage.py dbshell < words.sql
cd ..
sudo chgrp -R www-data sprint3
sudo chmod -R g+w sprint3
sudo apache2ctl restart
sudo systemctl restart runworkertest
sudo systemctl restart mydaphnetest
