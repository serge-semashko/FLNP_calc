import math
import matplotlib.pyplot as plt

import numpy as np
import matplotlib
import sys

# flog.write((len(sys.argv))
flog = open('log.txt', 'w')
fdata = open('out.txt', 'w')
flog.write(sys.executable)
if len(sys.argv) < 1:
    flog.write("using sys.executable <input data file>")
    exit(-1)
for i in sys.argv:
    flog.write(i)
startX = 10
shift_y = 10
add_y = 1
u_magnet = 400
round_signs = 6
m_elec = 9.1e-31
q_elec = 1.6e-19
k1 = 1000 * (m_elec / q_elec)
din = open(sys.argv[1], 'r')
inlines = din.readlines();
din.close()
size = inlines[0]
size = np.array(size.replace(' ', '').replace('\n', '').split('\t'), dtype=int);
w = size[0]
h = size[1]
bxy = np.zeros((h, w, 14))
flog.write('\nsize = ' + str(size))

flog.write(str(size))
splice_low = 0
tkp = np.zeros(w)
for i in range(2, len(inlines)):  # len(inlines) -37300
    y = (i - 2) % h
    x = (i - 2) // h
    i1 = inlines[i].replace(' ', '').replace('\n', '').split('\t');
    flog.write('====   %d [%d, %d]  = %s' % (i, y, x, inlines[i]))
    inda = [round(float(x), round_signs) for x in inlines[i].replace(' ', '').replace('\n', '').split('\t')]
    for add_i in range(10):
        inda.append(0)
    inda[1] = inda[1] + add_y;
    if inda[1] <= 0:
        splice_low = y
        bxy[y, x] = np.array(inda)
        # flog.write(('skip 1 %d %s'%())
        flog.write(('skip 1  nline %d  line(%d) = %s' % (x, i, inlines[i])))
        continue
    # flog.write((str(inda))
    # 4  Calc matrix B
    B = math.sqrt(inda[2] ** 2 + inda[3] ** 2)
    inda[4] = B

    # 5 Calc matrix R
    try:
        R = k1 * 1000 * (u_magnet / inda[1]) / inda[2] ** 2
        inda[5] = R
    except Exception as e:
        R = -131313
        inda[5] = -131313

        flog.write(('EXCEPTION R  Line %d  = %s  === %s \n' % (i, str(e), str(inda))))
    # 5  - 6 Calc matrix TKP
    try:
        if tkp[x] > 0:
            inda[6] = 1
        else:
            if R > inda[1]:
                inda[6] = 0
                tkp[x] = 0
            else:
                tkp[x] = 1
                inda[6] = 1
    except Exception as e:
        flog.write(('EXCEPTION TKP  Line %d  = %s  === %s \n' % (i, str(e), str(inda))))
    # 6 - 7 calc BxTKP
    inda[7] = inda[2] * inda[6]
    # 7 - 8 calc ByTKP
    inda[8] = inda[3] * inda[6]
    # 8 - 9 calc BTKP
    inda[9] = inda[4] * inda[6]

    # 9 - 10 calc BxTKP / B
    if abs(inda[4]) > 0.0000001:
        inda[10] = inda[7] / inda[4]
    flog.write('[%d,%d] ' % (y, x) + str(inda))
    bxy[y, x] = np.array(inda)









print('splice %d' % (shift_y))
nbxy = bxy[shift_y:, :]



nbxy = bxy
# nbxy = nbxy + [0, 5 ,0 ,0,0,0]
flog.write((str(bxy.shape)) + '\n')
flog.write((str(nbxy.shape)) + '\n')
nw, nh, nc = nbxy.shape



#*******************  Calc Ne
# calc max val on first row y>0 BxTKP
max_bxtkp = 0
for y in range(0, 60):
    y_val = (bxy[y][0][1])
    if (y_val*100)<=0:
        continue
    row = bxy[y,:,7]
    max_bxtkp = max(row)
    # print(str(max_bxtkp)+'      '+ str(row))
    break
#*******************  Calc Ne & He

for y in range(nw):
    for x in range(nh):
        nbxy[y,x,11] = nbxy[y,x,7] /max_bxtkp
        #  calc He
        nbxy[y,x,12] = nbxy[y,x,11] * nbxy[y,x,10]
line = 'Y      '
for x in range(w):
    line += " %6.2f" % (nbxy[0][x][0])
fdata.write(line + '\n')
for y in range(9, 60):
    line = "%4.2f " % (nbxy[y][0][1])
    for x in range(h):
        # line += "(%4.2f, %4.2f)" % (nbxy[y][x][0], nbxy[y][x][1])
        line += " %6.2f" % (nbxy[y][x][6])
        # line += "(%4.2f, %4.2f, %0.6f)" % (nbxy[y][x][0], nbxy[y][x][1], nbxy[y][x][2])
        # line += "(%4.2f,  %0.6f, %0.6f, %0.6f)" % (nbxy[y][x][0], nbxy[y][x][4], nbxy[y][x][5], nbxy[y][x][6])
    fdata.write(line + '\n')
line += '\nY      '
for x in range(w):
    line += " %6.2f" % (nbxy[0][x][0])
fdata.write(line + '\n')
flog.close()
fdata.close()





xarr = bxy[0:1, :, 0][0]
spls = bxy[0:1, :]
labelz = [' mm', ]

# print(str(spls))
steps = [1, 2, 5, 10, 20, 40, 60, 80]


def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


colors = [rgb_to_hex(0, 0, 125), rgb_to_hex(255, 0, 0), rgb_to_hex(146, 208, 80), rgb_to_hex(0, 176, 240),
          rgb_to_hex(247, 150, 70), rgb_to_hex(150, 150, 150), rgb_to_hex(50, 50, 50), rgb_to_hex(0, 0, 0)]
# steps = [1, 10]
fig, plots1 = plt.subplots(nrows=1, layout='constrained')
for i in steps:
    # print('I= ' + str(i))
    for y in range(nw):
        # print('bxy=' + str(bxy[y, 0, 1]))
        if int(i * 100) == int(bxy[y, 0, 1] * 100):
            step_num = steps.index(i)
            yl = bxy[y:y + 1, 1, 1]
            # print('i = ' + str(i) + ' yl =  ' + str(yl))
            bx = bxy[y:y + 1, :, 2][0]
            by = bxy[y:y + 1, :, 3][0]
            print(str())
            plots1.plot(xarr, bx, colors[step_num], label='bx ' + str(i) + labelz[0], linestyle='dashed')
            plots1.plot(xarr, by, colors[step_num], label='by ' + str(i) + labelz[0], linestyle='dotted')
            break

fig, plots2 = plt.subplots(nrows=1, layout='constrained')
for i in steps:
    # print('I= ' + str(i))
    for y in range(nw):
        # print('bxy=' + str(bxy[y, 0, 1]))
        if int(i * 100) == int(bxy[y, 0, 1] * 100):
            step_num = steps.index(i)
            yl = bxy[y:y + 1, 1, 1]
            # print('i = ' + str(i) + ' yl =  ' + str(yl))
            bx = bxy[y:y + 1, :, 7][0]
            by = bxy[y:y + 1, :, 8][0]
            b = bxy[y:y + 1, :, 9][0]
            print(str())
            plots2.plot(xarr, bx, colors[step_num], label='BxTKP ' + str(i) + labelz[0], linestyle='dashed')
            plots2.plot(xarr, by, colors[step_num], label='ByTKP ' + str(i) + labelz[0], linestyle='dotted')
            plots2.plot(xarr, b, colors[step_num], label='ByTKP ' + str(i) + labelz[0], linestyle='solid')
            break

fig, plots3 = plt.subplots(nrows=1, layout='constrained')
for i in steps:
    # print('I= ' + str(i))
    for y in range(nw):
        # print('bxy=' + str(bxy[y, 0, 1]))
        if int(i * 100) == int(bxy[y, 0, 1] * 100):
            step_num = steps.index(i)
            yl = bxy[y:y + 1, 1, 1]
            # print('i = ' + str(i) + ' yl =  ' + str(yl))
            bx_div_b = bxy[y:y + 1, :, 10][0]
            # print(str())
            plots3.plot(xarr, bx_div_b, colors[step_num], label=str(i) + labelz[0], linestyle='solid')
            break


fig, plots4 = plt.subplots(nrows=1, layout='constrained')
for i in steps:
    # print('I= ' + str(i))
    for y in range(nw):
        # print('bxy=' + str(bxy[y, 0, 1]))
        if int(i * 100) == int(bxy[y, 0, 1] * 100):
            step_num = steps.index(i)
            yl = bxy[y:y + 1, 1, 1]
            # print('i = ' + str(i) + ' yl =  ' + str(yl))
            ne = bxy[y:y + 1, :, 11][0]
            # print(str())
            plots4.plot(xarr, ne, colors[step_num], label=str(i) + labelz[0], linestyle='solid')
            break

fig, plots5 = plt.subplots(nrows=1, layout='constrained')
for i in steps:
    # print('I= ' + str(i))
    for y in range(nw):
        # print('bxy=' + str(bxy[y, 0, 1]))
        if int(i * 100) == int(bxy[y, 0, 1] * 100):
            step_num = steps.index(i)
            yl = bxy[y:y + 1, 1, 1]
            # print('i = ' + str(i) + ' yl =  ' + str(yl))
            he = bxy[y:y + 1, :, 12][0]
            # print(str())
            plots5.plot(xarr, he, colors[step_num], label=str(i) + labelz[0], linestyle='solid')
            break





# quit()
# print('y=' + str(y) + ' ' + str(xarr))
# print(str(bx))

plots1.set_title('BxBy')
plots1.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
              fancybox=True, shadow=True, ncol=1)
# plots1.legend()

plots2.set_title('BxTKP ByTKP')
# plots2.legend()
plots2.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
              fancybox=True, shadow=True, ncol=1)

plots3.set_title('BxTKP/B')
plots3.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
              fancybox=True, shadow=True, ncol=1)

plots4.set_title('NE')
plots4.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
              fancybox=True, shadow=True, ncol=1)

plots5.set_title('He')
plots5.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
              fancybox=True, shadow=True, ncol=1)




# plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
# plots1[1].legend()
plots1.grid()
plots2.grid()
plots3.grid()
plots4.grid()
plots5.grid()

# plt.grid()
plt.show()
