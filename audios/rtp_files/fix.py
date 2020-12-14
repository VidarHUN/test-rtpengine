import os

with open('amrnb_fv_to_mrsv0.hex.rtp', 'r') as f:
    time = 0.000000
    new_file = open('new_amr', 'a')
    for line in f:
        line.strip()
        new_line = line.split(" ")
        new_line[0] = '{:.6f}'.format(time)
        new_file.write(" ".join(new_line))
        time += 0.020000
    
new_file.close()
