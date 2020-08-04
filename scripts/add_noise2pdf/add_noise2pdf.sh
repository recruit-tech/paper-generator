#!/bin/bash

target_pdf=$1
target_dir=`dirname $target_pdf`
tmp_name=`basename $1`
base_name=${tmp_name%.*}

noiseA=noise_data/line_noise_1.png
noiseB=noise_data/line_noise_1c.png

# pdf -> png
pdftoppm -png $target_pdf $target_dir/$base_name

# add noise
for img in `ls $target_dir/$base_name*.png`
do
  out_img=$target_dir/out_n1_`basename $img`
  composite -compose over $noiseA $img $out_img
  out_img=$target_dir/out_n2_`basename $img`
  composite -compose over $noiseB $img $out_img
done

# rotate and create pdf
convert $target_dir/out_n1_$base_name*[0-9].png $target_dir/out_${base_name}_n1_r0.pdf
convert -rotate 1.5 $target_dir/out_n1_$base_name*[0-9].png $target_dir/out_${base_name}_n1_rr.pdf
convert -rotate -1.5 $target_dir/out_n1_$base_name*[0-9].png $target_dir/out_${base_name}_n1_rl.pdf
convert $target_dir/out_n2_$base_name*[0-9].png $target_dir/out_${base_name}_n2_r0.pdf
convert -rotate 1.5 $target_dir/out_n2_$base_name*[0-9].png $target_dir/out_${base_name}_n2_rr.pdf
convert -rotate -1.5 $target_dir/out_n2_$base_name*[0-9].png $target_dir/out_${base_name}_n2_rl.pdf

# delete file
rm $target_dir/out_n*_$base_name*[0-9].png
rm $target_dir/$base_name*[0-9].png

