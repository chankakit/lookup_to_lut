from PIL import Image
import numpy as np
import os, sys
import ntpath

import time

def header_info(lookup_name):
    header_infomation = '''#Created by: kit
TITLE \"{name}\"

#LUT size
LUT_3D_SIZE 64

#data domain
DOMAIN_MIN 0.0 0.0 0.0
DOMAIN_MAX 1.0 1.0 1.0

#LUT data points
'''
    return header_infomation.format(name = lookup_name)

def lookup64_to_lut(input_file):
    # load the lookup image and convert to numpy ndarray
    lookup_na = np.asarray(Image.open(input_file))
    white_na = np.ones((512, 512, 3)) * 255

    # inital output data array
    output_data_arr = np.array([])
    
    # calculate the result in numpy ndarray
    lookup_na = np.around(lookup_na / white_na, decimals = 6)

    # along the Y axis splite array, return a list contain 8 ndarray
    lookup_na_h = np.vsplit(lookup_na, 8)

    for i in range(8):
        temp_arr_v = np.hsplit(lookup_na_h[i], 8)
        for j in range(8):
            temp_single = temp_arr_v[j].copy()
            temp_single.shape = (1, 4096, 3)
            output_data_arr = np.append(output_data_arr, temp_single)

    return output_data_arr

def init_file(filename):
    with open(filename, 'w') as fp:
        fp.writelines(header_info(ntpath.basename(lookup_image_filepath)[:-4]))
    fp.closed

def write_data(lut_data, output_file):
    with open(output_file, 'a') as fp:
        for i in range(len(lut_data)):
            fp.write("%.6f" % (lut_data[i]))
            if (i % 3) == 2:
                fp.write("\n")
            else:
                fp.write(" ")
    fp.closed
    # lut_data.tofile(output_file, sep=" ", format="%10.6f")


if __name__ == "__main__":
    start = time.time()
    
    lookup_image_filepath = sys.argv[1]
    output_file_name = lookup_image_filepath[:-3] + 'CUBE'

    init_file(output_file_name)
    write_data(lookup64_to_lut(lookup_image_filepath), output_file_name)

    end = time.time()
    print("Done in %.2f s." % (end - start))
