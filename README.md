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
Job Queue
* A queue that holds the jobs meant to be executed

CPU Idle Table
* an array that contains a boolean 1 or 0 relating to if the processor it corresponds to is busy or idle. 

##### This design uses n + 2 pipes (n is number of cpus).
Server fifo
* Used to send jobs to the server from the user.

Processor-done fifo
* All of the processors write to this single fifo with their CPU ID number when they have completed their job

Processor-job fifo
* Each processor is assigned its own processor-job fifo
* Each processor reads from this pipe to get its new updated job

##### Main looping cycle
The base of the design is a loop that constantly checks for new jobs from the server fifo and processors that finished from the processor done fifo.

Whenever a new job comes from the server fifo, the server will add it to a job queue. The server will check each entry in the CPU idle table until either there is an idle cpu found, or no idle cpus exist. If an idle CPU is found, the job is popped from the job queue sent via a unique processor job fifo. If no idle cpu is found, no action is taken after adding the job to the job queue.

Whenever a value is sent to, and read from, the processor done fifo, the server opens an entry in the cpu idle table for the specific cpu and then attempts to pop an element from the job queue if there is one available and assign the job to the newly idle cpu.

## Testing

Run the scripts using this command
```sh
$ cd dillinger
$ npm install -d
$ node app
```
