# [Advent of Code 2022](https://adventofcode.com/2022)

## Generate files for Day `<n>` from templates

```
> ./newday.sh <n>
```

## Python 3

```sh
> python day<n>.py
```

## C++
```
> mkdir test_build
> g++ -o test_build/day<n> day<n>.cpp -Ltest_build -lgtest -lgtest_main -pthread -std=c++0x && test_build/day<n>
```
