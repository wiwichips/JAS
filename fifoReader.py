import os
import sys
import select

# extract server fifo string
fifo_s=sys.argv[1]
PName=sys.argv[0]

# let the user know if the number of arguments is incorrect
if len(sys.argv) != 2:
  print(PName + ": Need to have one argument not " + str(sys.argv[1:]))
  exit(0)

# let the user know if there is an error opening the pipe
try:
  fifo_s_fd = os.open(fifo_s, os.O_NONBLOCK)
except:
  print(PName + ": Not able to open " + fifo_s)
  exit(0)

# get the readable, writable and exceptional lists from select
RWE = select.select([fifo_s_fd], [], [], 0.001)

if RWE[0]:
  for RWE_fd in RWE: 
    if RWE_fd:
      print(os.read(RWE_fd[0], 1024).decode('ASCII'))

# close the file descriptior
os.close(fifo_s_fd)
