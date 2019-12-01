import pandas as pd
import os

test_csv = "../data/annotations/test_labels.csv"
'''
test_labels.csv has the following format 
filename, width, height, class, xmin, ymin, xmax, ymax
WIDER_val/images/2--Demonstration/2_Demonstration_Protesters_2_456.jpg,1024,683,face,765,514,811,568

output ground truth file should have the format
face 765 514 811 568
'''
df = pd.read_csv(test_csv)

print(df.head())
gt_folder = "../metrics/Object-Detection-Metrics/groundtruths-faces"


filenames = df['filename']
ws = df['width']
hs = df['height']
class_names = df['class']
xmins = df['xmin']
ymins = df['ymin']
xmaxs = df['xmax']
ymaxs = df['ymax']

for i, filename in enumerate(filenames):
    file = filename.split("/")[-1].split(".")[0] + ".txt"
    class_name = class_names[i]
    xmin = xmins[i]
    ymin = ymins[i]
    xmax = xmaxs[i]
    ymax = ymaxs[i]

    content = "{0} {1} {2} {3} {4}\n".format(class_name, xmin, ymin, xmax, ymax)
    out_file = os.path.join(gt_folder, file)
    with open(out_file,'a+') as f:
        f.write(content)



# with open(file_path, "r") as f:
#     for line in f.readlines():
#         line = line.replace('\n','')
#         content = line.split(",")
#         print(content)
