# PDF file processing tool (scripts for command line)
tools / script

## Required Module
(for ubuntu)

* pdftoppam
```
$ sudo apt install xpdf
```

* convert
```
$ sudo apt install imagemagick
```

## **add noise to pdf**
### USAGE
```
$ ./add_noise2pdf.sh sample.pdf
```
```
$ ./add_noise2pdf_files.sh hoge/huga/abc*.pdf
```

### OUTPUT
This script images a PDF file and adds noise and rotation.

**out\_sample\_xx.pdf**

* noise 2 patterns
filename: n1, n2

* rotate 3 patterns
fileneme: r0(rotate 0), rr(rotate right), rl(rotate left)

ex:out\_sample\_n1_r0.pdf

out\_: output  
n1: noise #1  
r0: rotate 0

