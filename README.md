# Job Assistance Scheduler (JAS)
CIS-3050 A2
2020-10-29

## Design

```
                           +->-<-processor1
mgSubmit ->- mgServer ->-<-+->-<-processor2
                           +->-<-processor3
```
##### Data Structures
Server fifo
* Used to send jobs to the server from the user.

Processor-done fifo
* All of the processors write to this single fifo with their CPU ID number when they have completed their job

Processor-job fifo
* Each processor is assigned its own processor-job fifo
* Each processor reads from this pipe to get its new updated job

##### This design uses n + 2 pipes (n is number of cpus).
Server fifo
* Used to send jobs to the server from the user.

Processor-done fifo
* All of the processors write to this single fifo with their CPU ID number when they have completed a job

Processor-job fifo
* Each processor is assigned its own processor-job fifo
* Each processor reads from this pipe to get its new updated job

##### Main looping cycle
The base of the design is a loop that constantly checks for new jobs from the server fifo and processors that finished from the processor done fifo.

Whenever a new job comes from the server fifo, the server will add it to a job queue. The server will check each entry in the CPU idle table until either there is an idle cpu found, or no idle cpus exist. If an idle CPU is found, the job is popped from the job queue sent via a unique processor job fifo. If no idle cpu is found, no action is taken after adding the job to the job queue.

Whenever a value is sent to, and read from, the processor done fifo, the server opens an entry in the cpu idle table for the specific cpu and then attempts to pop an element from the job queue if there is one available and assign the job to the newly idle cpu.

## Testing
##### Usage
Run the testing script using the command:
```sh
$ ./runtests n # the n represents the test number
```
Refer to the expected output at the bottom of this file as a benchmark for comparison. 

##### Test Case 1 
```sh
$ ./runtests 1
```
Objective: This test checks if multiple arguments are properly sent to each processor by running the command ps -s and ps. The output of the logs for the first two processors will be shown after running the commands..
Expected Output: ps output in different formats, one using -s and one without any flags.
Success: The test passes if the commands look different. 

##### Test Case 2
```sh
$ ./runtests 2
```
Objective: This test checks for garbage handling, executing a normal command, status and shutdown. 
Expected Output: the status reports two jobs have completed and all cpus are idle. No more fifos are left after -x is sent.
Success: This test is a success if the status says the program system doesn't crash with garbage input, displays 2 jobs have completed and the server closes with -x and properly cleans up the pipes.

##### Test Case 3
```sh
$ ./runtests 3
```
Objective: This test checks if the server can properly maintain a job queue with jobs that take a certain amount of time to complete where there are more jobs than processors.
Expected output: Status reporting all jobs have finished and every cpu is idle.
Success: Assuming an 8 processor machine, this test is a a success if the first status shows 8 processors are busy and the second status says 12 jobs have completed.

##### Test Case 4
```sh
$ ./runtests 4
```
Objective: This test checks if each processor can handle globbing. ls mg* is sent to the server. 
Expected output: a list of files that all start with mg.
Success: If the log file contains only files that start with mg (mgSubmit, mgServer, and mgProcess), the test is a success.

##### Expected Output for each test case ./runTests all
Details will not be an exact match on all systems depending on what processes are running on the system and how many physical cpus are on the system. But this output can be used as a baseline for expected output.

The tests are meant to be run one after another, but you can run ``./runTests all`` to run all the tests at once in order.
```bash

./runTests:	~~~~~~~~~~~~~~
./runTests:	Running test 1
./runTests:	~~~~~~~~~~~~~~

Shutting down...



TEST1:	PRINTING HEAD OF PROCESSOR 1 LOG WITH COMMAND ps

  PID TTY          TIME CMD
14258 pts/1    00:00:00 runTests
14260 pts/1    00:00:00 mgServer
14267 pts/1    00:00:00 mgProcessor
14269 pts/1    00:00:00 mgProcessor
14271 pts/1    00:00:00 mgProcessor
14273 pts/1    00:00:00 mgProcessor
14275 pts/1    00:00:00 mgProcessor
14277 pts/1    00:00:00 mgProcessor
14279 pts/1    00:00:00 mgProcessor



TEST1:	PRINTING HEAD OF PROCESSOR 2 LOG WITH COMMAND ps -s

  UID   PID          PENDING          BLOCKED          IGNORED           CAUGHT STAT TTY        TIME COMMAND
 1000  2444 0000000000000000 0000000000000000 0000000000001000 0000000180014000 Ssl+ tty2       0:00 /usr/lib/gdm3/gdm-x-session --run-script i3
 1000  2446 0000000000000000 0000000000000000 0000000000001000 00000001c18066ef Sl+  tty2      21:03 /usr/lib/xorg/Xorg vt2 -displayfd 3 -auth /run/user/1000/gdm/Xauthority -background none -noreset -keeptty -verbose 3
 1000  2462 0000000000000000 0000000000000000 0000000000001000 00000001800166af S+   tty2       0:35 i3
 1000 14258 0000000000000000 0000000000010000 0000000000000084 0000000000010002 S+   pts/1      0:00 /bin/bash ./runTests all
 1000 14260 0000000000010000 0000000000010000 0000000000000086 0000000043817e79 S+   pts/1      0:00 /bin/bash ./mgServer
 1000 14267 0000000000000000 0000000000010000 0000000000000086 0000000000010000 S+   pts/1      0:00 /bin/bash ./mgProcessor 1 14260
 1000 14269 0000000000000000 0000000000010000 0000000000000086 0000000000010000 S+   pts/1      0:00 /bin/bash ./mgProcessor 2 14260
 1000 14271 0000000000000000 0000000000000000 0000000000000086 0000000000010000 S+   pts/1      0:00 /bin/bash ./mgProcessor 3 14260
 1000 14273 0000000000000000 0000000000000000 0000000000000086 0000000000010000 S+   pts/1      0:00 /bin/bash ./mgProcessor 4 14260



TEST1:	Test passes if the two outputs are in a different format.

./runTests:	~~~~~~~~~~~~~~
./runTests:	Running test 2
./runTests:	~~~~~~~~~~~~~~

There are 8 processors
2 jobs have been completed
1: idle
2: idle
3: idle
4: idle
5: idle
6: idle
7: idle
8: idle
Shutting down...
TEST2:	Test passes if Status above should say 2 jobs have been completed and program exits
TEST2:	Check the /tmp/ directory to ensure the fifps have properly closed for the current user

./runTests:	~~~~~~~~~~~~~~
./runTests:	Running test 3
./runTests:	~~~~~~~~~~~~~~

TEST3:	Waiting three seconds before checking the server status
TEST3:	____________
TEST3:	############
TEST3:	Printing Status
There are 8 processors
12 jobs have been completed
1: idle
2: idle
3: idle
4: idle
5: idle
6: idle
7: idle
8: idle
Shutting down...
TEST3:	Test passed if the status displays 12 jobs have been completed and all jobs are idle

./runTests:	~~~~~~~~~~~~~~
./runTests:	Running test 4
./runTests:	~~~~~~~~~~~~~~

Shutting down...



TEST4:	PRINTING cat OF PROCESSOR 1 LOG WITH COMMAND ls mg*

mgProcessor
mgServer
mgSubmit



TEST4:	Test passes if only files starting with mg are listed.

./runTests:	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
./runTests:	If there were any problems, please try running each test individually.
./runTests:	Run tests on their own by typing ./runTests 1 for example.
./runTests:	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
./runTests:	~~~~~~~~~~~~~~~~~~~~~~~~~~~ALL TESTS PASSED~~~~~~~~~~~~~~~~~~~~~~~~~~~

```

## Works Cited
The timedCountdown script was not created by me. It was provided by Andrew Hamilton-Wright for use in this assignment testing.

## Extension
I was granted a 24 hour extension on this assignment.
