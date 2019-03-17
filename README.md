# os project
## name: 刘彬 11612121
### task1：
* Data structures and functions:  
in the struct thread  add one member, named the thread_time,to record how much time the thread sleep.  
when the thread is created ,the thread_time set 0.  
``` c
void thread_time_check (struct thread *t, void *aux UNUSED)  
//to check the thread_time > 0, if thread_time == 0, to run.  
```
  
* Algorithms:  
		when the thread is created the thread_time set 0  
		then to calculate the thread_time(before it has been set ticks)  
		if the thread_time == 0 ,run this thread  
		else continue to calculate it  
	
* Synchronization:  
		because every thread has it thread_time not the global variable, so the algorithms is security.  
		
* Rationale:  
		in order to aviod the thread run and sleep much times, so to check the thread_time, if thread_time == 0 ,to run, not run and sleep
	
### task2：  
* Data structures and functions：  
		Priority queue:for ready list and semaphore wait queues and condition waiters queues  
``` c
bool thread_cmp_priority(const struct list_elem *a, const struct list_elem *b, void *aux UNUSED)
// to compare the priority  
void thread_hold_the_lock(struct lock *lock)  
// if the lock‘s priority > thread's priority ,let the thread's priority = lock's priority  
void thread_donate_priority (struct thread *t)  
// increase the thread's priority  
void thread_remove_lock (struct lock *lock)  
// remove the lock and change the thread's priority  
void thread_update_priority (struct thread *t)  
// update the thread's priority  
 ```
	
* Algorithms:   
		(1)when creat thread or change thread's priority change the order of  ready list(using method:list_insert_ordered)  
		(2)if a thread A get a lock B, and the A's priority < B's priority increase the priority of the lock,if locks are limited by other locks, then recursively increase their priority  
		(3)If a low-priority thread has the resources required by other high-priority threads, raise the priority of the low-priority thread to the highest priority of those threads  
		(4)if a thread is Donated status, if the new priority > current priority,change the current priority = new priority,else when the thread recover, recover the priority  
		(5)Implement semaphore wait queues and condition waiters queues as priority queues.  
		(6)Release locks that change the priority of a lock should take into account the remaining donated priorities and current priorities as well as preemption  
	
* Synchronization:  
		first, the priority queue implement the high-priority thread run first, it is a public address, so when multiple threads change their priority, just can one by one   
	
* Rationale:  
		In order to prevent the lower priority thread to get resources, because it could not run don't release resources, so that the high priority to occupy CPU without resources, use priority to donate, the higher priority thread priority to low priority thread, let him run release resources, make originally the higher priority thread to run, to prevent thread lock
	
### task3:  
* Data structures and functions:  
		implement floating point arithmetic
		
* Algorithms:  
		𝑝𝑟𝑖𝑜𝑟𝑖𝑡𝑦=𝑃𝑅𝐼_𝑀𝐴𝑋−(𝑟𝑒𝑐𝑒𝑛𝑡_𝑐𝑝𝑢/4)−(𝑛𝑖𝑐𝑒×2)
		𝑟𝑒𝑐𝑒𝑛𝑡_𝑐𝑝𝑢(𝑡) =𝑎×𝑟𝑒𝑐𝑒𝑛𝑡_𝑐𝑝𝑢(𝑡−1) +𝑓(𝑡) 

*	Synchronization:  
		same to task2 ,just need to change thread's priority, so no race
*	Rationale:  
		Recent_cpu can compute the value of recent_cpu and priority at the end of each slice, so as to determine which thread is running next, recent_cpu can lower the priority of recently run threads, and low-priority threads can be scheduled


