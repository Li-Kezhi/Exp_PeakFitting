#!/usr/bin/env python
# # -*- coding:utf-8 -*-

"""
Flowmeter converter program
"""

__author__ = "LI Kezhi"
__date__ = "$2017-12-02$"
__version__ = "1.0.1"

import Tkinter as tk

root = tk.Tk()
root.title('GC-MS配气柜流量计换算')

topframe = tk.Frame(root)
topframe.pack(side=tk.TOP)
bottomframe = tk.Frame(root)
bottomframe.pack(side=tk.BOTTOM)

leftframe = tk.Frame(topframe)
leftframe.pack(side=tk.LEFT)
rightframe = tk.Frame(topframe)
rightframe.pack(side=tk.RIGHT)
empty = tk.Label(topframe, text='          ')
empty.pack(side=tk.RIGHT)

leftlabel = tk.Label(leftframe, text='已知流量（mL/min）求流量计示数')
leftlabel.grid(row=0, column=0, columnspan=3)
leftlabel1 = tk.Label(leftframe, text='30 SCCM').grid(row=1, column=0)
leftlabel2 = tk.Label(leftframe, text='50 SCCM').grid(row=2, column=0)
leftlabel3 = tk.Label(leftframe, text='300 SCCM').grid(row=3, column=0)
leftlabel4 = tk.Label(leftframe, text='1 SLM').grid(row=4, column=0)
leftv1 = tk.StringVar()
leftv2 = tk.StringVar()
leftv3 = tk.StringVar()
leftv4 = tk.StringVar()
leftv1.set('20')
leftv2.set('30')
leftv3.set('100')
leftv4.set('400')
leftentry1 = tk.Entry(leftframe, textvariable=leftv1, width=5).grid(row=1, column=1)
leftentry2 = tk.Entry(leftframe, textvariable=leftv2, width=5).grid(row=2, column=1)
leftentry3 = tk.Entry(leftframe, textvariable=leftv3, width=5).grid(row=3, column=1)
leftentry4 = tk.Entry(leftframe, textvariable=leftv4, width=5).grid(row=4, column=1)
leftout1 = tk.Label(leftframe, text='0', width=5).grid(row=1, column=2)
leftout2 = tk.Label(leftframe, text='0', width=5).grid(row=2, column=2)
leftout3 = tk.Label(leftframe, text='0', width=5).grid(row=3, column=2)
leftout4 = tk.Label(leftframe, text='0', width=5).grid(row=4, column=2)

rightlabel = tk.Label(rightframe, text='已知流量计示数求流量（mL/min）')
rightlabel.grid(row=0, column=0, columnspan=3)
rightlabel1 = tk.Label(rightframe, text='30 SCCM').grid(row=1, column=0)
rightlabel2 = tk.Label(rightframe, text='50 SCCM').grid(row=2, column=0)
rightlabel3 = tk.Label(rightframe, text='300 SCCM').grid(row=3, column=0)
rightlabel4 = tk.Label(rightframe, text='1 SLM').grid(row=4, column=0)
rightv1 = tk.StringVar()
rightv2 = tk.StringVar()
rightv3 = tk.StringVar()
rightv4 = tk.StringVar()
rightv1.set('50')
rightv2.set('20')
rightv3.set('80')
rightv4.set('200')
rightentry1 = tk.Entry(rightframe, textvariable=rightv1, width=5).grid(row=1, column=1)
rightentry2 = tk.Entry(rightframe, textvariable=rightv2, width=5).grid(row=2, column=1)
rightentry3 = tk.Entry(rightframe, textvariable=rightv3, width=5).grid(row=3, column=1)
rightentry4 = tk.Entry(rightframe, textvariable=rightv4, width=5).grid(row=4, column=1)
rightout1 = tk.Label(rightframe, text='0', width=5).grid(row=1, column=2)
rightout2 = tk.Label(rightframe, text='0', width=5).grid(row=2, column=2)
rightout3 = tk.Label(rightframe, text='0', width=5).grid(row=3, column=2)
rightout4 = tk.Label(rightframe, text='0', width=5).grid(row=4, column=2)

def calc():
    in1 = float(leftv1.get())
    in2 = float(leftv2.get())
    in3 = float(leftv3.get())
    in4 = float(leftv4.get())
    out1 = (in1 + 0.3369) / 0.1901
    out2 = (in2 - 8.4871) / 0.6239
    out3 = (in3 - 5.3294) / 1.0147
    out4 = (in4 + 27.145) / 2.1568
    out1 = '%.1f' % out1
    out2 = '%.1f' % out2
    out3 = '%.1f' % out3
    out4 = '%.1f' % out4
    leftout1 = tk.Label(leftframe, text=out1, width=5).grid(row=1, column=2)
    leftout2 = tk.Label(leftframe, text=out2, width=5).grid(row=2, column=2)
    leftout3 = tk.Label(leftframe, text=out3, width=5).grid(row=3, column=2)
    leftout4 = tk.Label(leftframe, text=out4, width=5).grid(row=4, column=2)

    in1 = float(rightv1.get())
    in2 = float(rightv2.get())
    in3 = float(rightv3.get())
    in4 = float(rightv4.get())
    out1 = in1 * 0.1901 - 0.3369
    out2 = in2 * 0.6239 + 8.4871
    out3 = in3 * 1.0147 + 5.3294
    out4 = in4 * 2.1568 - 27.145
    out1 = '%.1f' % out1
    out2 = '%.1f' % out2
    out3 = '%.1f' % out3
    out4 = '%.1f' % out4
    rightout1 = tk.Label(rightframe, text=out1, width=5).grid(row=1, column=2)
    rightout2 = tk.Label(rightframe, text=out2, width=5).grid(row=2, column=2)
    rightout3 = tk.Label(rightframe, text=out3, width=5).grid(row=3, column=2)
    rightout4 = tk.Label(rightframe, text=out4, width=5).grid(row=4, column=2)

B = tk.Button(bottomframe, text ="计算", command = calc)

B.pack()
root.mainloop()