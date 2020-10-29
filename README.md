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
Run a the server in one terminal with the command:
```sh
$ ./mgServer
```
Run the testing script in another terminal using the command:
```sh
$ ./runtests n # the n represents the test number
```

##### Test Case 1 
```sh
$ ./runtests 1
```
This test checks if multiple arguments are properly sent to each processor by running the command ps -s and ps. The output of the logs for the first two processors will be shown after running the commands, if they are different, the test has passed.

##### Test Case 2
Run a the server in one terminal with the command:
```sh
$ ./mgServer
```
Run the testing script in another terminal using the command:
```sh
$ ./runtests 2
```
This test checks for garbage handling, executing a normal command, status and shutdown. This test is a success if the status says the program system doesn't crash with garbage input, displays 2 jobs have completed and the server closes with -x and properly cleans up the pipes.

##### Test Case 3
Run a the server in one terminal with the command:
```sh
$ ./mgServer
```
Run the testing script in another terminal using the command:
```sh
$ ./runtests 3
```
This test checks if the server can properly maintain a job queue with jobs that take a certain amount of time to complete. This test is a a success if the first status shows 8 processors are busy and the second status says 12 jobs have completed.

