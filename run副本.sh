source pandas/bin/activate
python compute.py run 592_nc279__PTLs15_line3 False 
python compute.py run 592_nc279 False 
python compute.py run 592 False 
python compute.py image 592_nc279__PTLs15_line3 False
python compute.py image 592_nc279 False
python compute.py image 592 False

python reform_output.py output
