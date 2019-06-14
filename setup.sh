#!/bin/bash
template new template "$1"
mv ./* "../../$1"
cd ..
rmdir ducktemplate
