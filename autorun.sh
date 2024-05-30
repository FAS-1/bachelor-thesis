#!/bin/bash
set -e

if [[ $# -ne 2 ]];
then
    echo "usage: $0 <Set-Nr> <Scheduling Algorithm>"
    exit 1
fi

SET=$1
ALGO=$2

LINK=static
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/$ALGO-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/$ALGO-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/$ALGO-$LINK/$i/
done

LINK=longestpathfirst
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/$ALGO-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/$ALGO-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/$ALGO-$LINK/$i/
done

LINK=demandfirst
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/$ALGO-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/$ALGO-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/$ALGO-$LINK/$i/
done
