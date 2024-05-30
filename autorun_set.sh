#!/bin/bash
set -e

if [[ $# -ne 1 ]];
then
    echo "usage: $0 <Set-Nr>"
    exit 1
fi

SET=$1

LINK=static
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/rr-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/rr-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/rr-$LINK/$i/
done

LINK=longestpathfirst
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/rr-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/rr-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/rr-$LINK/$i/
done

LINK=demandfirst
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/rr-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/rr-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/rr-$LINK/$i/
done

LINK=static
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/sjf-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/sjf-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/sjf-$LINK/$i/
done

LINK=longestpathfirst
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/sjf-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/sjf-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/sjf-$LINK/$i/
done

LINK=demandfirst
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/sjf-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/sjf-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/sjf-$LINK/$i/
done

LINK=static
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/prio-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/prio-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/prio-$LINK/$i/
done

LINK=longestpathfirst
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/prio-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/prio-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/prio-$LINK/$i/
done

LINK=demandfirst
for i in {1..10};
do
  source ../venv/ipmininet/bin/activate
  python experiments/src/$SET/prio-$LINK.py
  deactivate

  mkdir -p experiments/results/$SET/prio-$LINK/$i

  mv experiments/results/h* experiments/results/$SET/prio-$LINK/$i/
done