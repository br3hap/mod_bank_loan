#!/bin/bash

echo "Agregando archivos al staging area..."
git add .

echo "Haciendo commit..."
git commit -m "upload change"

echo "Haciendo push al repositorio..."
git push --set-upstream origin master
