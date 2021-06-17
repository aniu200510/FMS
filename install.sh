#!/bin/bash

#
#  Funding management system installation instructions.
#

pro_root='/opt/cfiec/fms/'
pro='/opt/cfiec/'
python_home=`which python3`


init_pro(){
	if [ ! -d ${pro} ];
	then
		sudo mkdir -p ${pro} >/dev/null
	fi
	sudo chown ${who}.${who} ${pro}
	if [ ! -d ${pro_root} ];
	then
		mkdir -p ${pro_root} >/dev/null 
	fi
}

env_virtual(){
    if [ ! -d ${pro_root}.venv ];
	then
		mkdir ${pro_root}.venv >/dev/null 
	fi
	sudo apt-get install -y python3-venv >/dev/null
	${python_home} -m venv $pro_root.venv >/dev/null  #必须是python3才支持venv
    ${pro_root}.venv/bin/pip install billiard==3.5.0.5 >/dev/null 2>&1
    ${pro_root}.venv/bin/pip install coverage >/dev/null 2>&1
	${pro_root}.venv/bin/pip install -r ./requirements/requirements.txt
	${pro_root}.venv/bin/pip install -r ./requirements/requirements-pyecharts.txt
}


cp_py() {
    # rsync all source code
    rsync -avz  --exclude .git/ --exclude tmp/ . ${pro_root}
}

create_db(){
    sudo -u postgres psql -c 'CREATE DATABASE "fms";'
    sudo -u postgres psql -c "CREATE USER funder WITH PASSWORD 'funder1017';"
    sudo -u postgres psql -c 'ALTER USER funder CREATEDB;'
    sudo -u postgres psql -c 'ALTER ROLE funder SET client_encoding TO "utf8";'
    sudo -u postgres psql -c 'ALTER ROLE funder SET default_transaction_isolation TO "read committed";'
    sudo -u postgres psql -c 'ALTER ROLE funder SET timezone TO "Asia/Shanghai";'
    sudo -u postgres psql -c 'GRANT ALL PRIVILEGES ON DATABASE "fms" TO funder;'
}

celery(){
    sudo cp ./etc/fms.service /etc/systemd/system/ >/dev/null
    sudo systemctl daemon-reload
    sudo systemctl enable fms >/dev/null 2>&1
    sudo systemctl restart fms.service >/dev/null 
}

help(){
	echo "usage: $0 help"
	echo "       $0 (all|update|single)"
	cat <<EOF

	help       - this screen
	update     - update the pyc only
	all        - install first time all in
EOF
}


case "$1" in
    update)
        cp_py
        migrate
        ;;
    dev)
        init_pro
        cp_py
        env_virtual
        create_db
        celery
        ;;
    all)
        init_pro
        cp_py
        env_virtual
        create_db
        celery
        ;;
    *)
        help
        ;;
esac

echo "...install end"
