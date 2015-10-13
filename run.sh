source pandas/bin/activate

files=(del-1_repeat/592 del-1_repeat/592_nc279 del-1_repeat/592_nc279_pTL15_line3 del-1_repeat/592_nc279_pTL20_line3)
time=$(date +%Y%m%d%H%M)
output="output_"${time}
mkdir $output
# reform data
for f in ${files[*]}
do
python help.py $f
done

# run computation
for f in ${files[*]}
do
python compute.py run $f False $output
done
# output images
#for f in ${files[*]}
#do
#python compute.py image $f False
#done

#read -n1 -r -p "Put all output data into 'output' folder, then press any key to continue..." key

# gene
python reform_output.py $output random

#plot selection distribution
python compute.py plot $output

