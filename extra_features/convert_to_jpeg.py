import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def convert_to_jpeg(image, output_path="testjpegconversion"):
    input_path = os.path.abspath(f"Input/Icon/{image}")
    img = cv2.imread(input_path)
    output_path = os.path.abspath(f"Output/OtherFeatures/{output_path}.jpeg")
    cv2.imwrite(output_path, img)
    return