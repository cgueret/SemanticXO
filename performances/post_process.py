'''
Created on 5 Oct 2011

@author: cgueret
'''

files=['output-time-write.csv', 'output-time-read.csv', 'output-space.csv']

def post_process():
    avg = {}
    for file in files:
        runs = []
        for line in open('%s' % file, 'r').readlines():
            runs.append(line.split(','))
        avg[file] = []
        for res_idx in range(0, len(runs[0])-1):
            res = 0.0
            for run_idx in range(0, len(runs)):
                 res += float(runs[run_idx][res_idx])
            res = res / len(runs)
            avg[file].append(float("%.4f" % res))
    
    keys = sorted(avg.keys())
    f = open('averages.dat', 'w')
    f.write("# run ")
    f.write(" ".join(keys))
    f.write("\n")
    for idx in range(0, len(avg[keys[0]])):
        f.write("%d " % idx)
        for key in keys:
            f.write("%f " % avg[key][idx])
        f.write("\n")
    f.close()

if __name__ == '__main__':
    post_process()