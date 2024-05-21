#!/bin/bash

# Script utilizado para criar o banco de dados
# O banco de dados atual sera removido!!!

# remove todos os arquivos de migração
#echo -n "Removendo arquivos de migração... "
#find . -path "../*/migrations/*.py" -not -name "__init__.py" -delete
#find . -path "../*/migrations/*.pyc" -delete
#echo "OK"

# remove o banco de dados atual
#echo -n "Removendo banco de dados... "
#rm "../db.sqlite3"
#echo "OK"

# cria novamente o banco de dados
#echo "Recriando banco de dados... "
#python3 ../manage.py makemigrations
#python3 ../manage.py migrate

# popula o banco de dados
echo "Populando o banco de dados... "
python3 ../manage.py shell < populator.py
echo "OK"

# corrige as permissões do banco de dados
#chmod uog+w ../db.sqlite3 

#pkill -f ../repository/manager/server.py

echo "\nBanco de dados recriado com sucesso."

