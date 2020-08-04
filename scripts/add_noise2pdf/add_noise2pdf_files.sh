#!/bin/bash

run_command='./add_noise2pdf.sh'

# add noise
for pdf in $@
do
  echo "target: $pdf"
  bash $run_command $pdf
done

