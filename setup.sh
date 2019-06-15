#!/bin/bash
template new template "$1"
mv ./* "../../$1"
cd ..
rmdir ducktemplate
cd "../$1"
git add ./*
git commit -m "Add ducks"
