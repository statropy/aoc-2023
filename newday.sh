#!/bin/zsh
echo "Creating files for Day $1"
touch input$1.txt
touch test$1.txt
sed "s/{{n}}/$1/g" template.src > day$1.py 
sed "s/{{n}}/$1/g" cpp.src > cpp/day$1.cpp
