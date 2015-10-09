source pandas/bin/activate

files=(data/592 data/unc-8 data/unc-8_pTL5_line1 data/unc-8_pTL17_line1)

# reform data
for f in ${files[*]}
do
python help.py $f
done

# run computation
for f in ${files[*]}
do
python compute.py run $f False
done
# output images
for f in ${files[*]}
do
python compute.py image $f False
done

read -n1 -r -p "Put all output data into 'output' folder, then press any key to continue..." key

# gene
python reform_output.py output random
