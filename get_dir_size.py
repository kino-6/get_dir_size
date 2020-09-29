import os, sys
import pprint
import numpy

cef_mb = 1024*1024

if len(sys.argv) == 2:
	walk_path = sys.argv[1]
else:
	walk_path = os.getcwd()

print("walk path = " , walk_path)

def get_dir_size(path='.'):
    total = 0.0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def get_size(path='.'):
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        return get_dir_size(path)

dic = {}
for foldername, subfolders, filenames in os.walk(walk_path):		
	for subfolder in subfolders:
		full_path = foldername + '\\' + subfolder
		dic[full_path] = get_size(full_path)/cef_mb

	for filename in filenames:
		full_path = foldername + '\\' + filename
		if os.path.islink(full_path):
			continue
		else:
			dic[full_path] = get_size(full_path)/cef_mb

sum = numpy.sum(numpy.array(list(dic.values())))
print("sum = {0:.4f} MB".format(sum))

sorted_size = sorted(dic.items(), key=lambda x:x[1], reverse=True)

top_x = 10
print("Top: {0}".format(top_x))
pprint.pprint(sorted_size[0:top_x])

log_file_path = "file_size.csv"
log_file = open(os.getcwd() + "\\" + log_file_path, 'w')
log_file.write("path,size\n")
for info in sorted_size:
	#line = {1} + "," + {2} + " % " + "( " +str(info[1]) + "[kb] )" + "\n").format((info[0]), str(info[1]/sum*100))
	line = "{0} , {1:.2f} % ({2:.4f}[MB])\n".format(info[0], info[1]/sum*100, info[1])
	log_file.write(line)
log_file.close()


