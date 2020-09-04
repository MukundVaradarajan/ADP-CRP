import sys
sys.stdin=open('/home/mukund/Competitive Coding/input.txt','r')
sys.stdout=open('/home/mukund/Competitive Coding/output.txt','w')

from time import time
start=time()

#GC instance
N=[4,4,3]
no_of_cars=sum(N)							#Cars per conveyor

C=[[1,2,3],[1,3],[1,2]]
changeover_cost=[[0,3,2],[4,0,3],[5,4,0]]
Conveyor=[[1,2,1,3],[1,3,3,1],[2,2,1]]	#First element at each conveyor retrievable
no_of_conveyors=len(Conveyor)
no_of_colours=len(changeover_cost)

min_cost=[]									#DP Array
retrieved_cars=[0 for x in range(no_of_conveyors)]

stage_queue=[]								#To load next stage with its states into algo
state_set=[]								#List of all states
infinity=1000000							#Infinity


#Find all possible states from current state
def find_all_next(state):
	all=[]
	k=0
	if sum(N)!=sum(state[:len(state)-1]):
		for i in range(len(state)-1):
			new=state.copy()
			if new[k]<N[k]:
				new[k]+=1
				k+=1
				new[-1]=k
				all.append(new)
			else:
				k+=1
	else:
		new=state.copy()
		new[-1]=0
		all.append(new)
	return all

s=[]										#Initial dummy state
for x in range(no_of_conveyors+1):
	s.append(0)
state_set.append(s)
stage=[]
stage.append(s)
stage_queue.append(stage)
min_cost.append((0,-1))

#DP Procedure
for stage_iter in range(no_of_cars+1):
	states_list=stage_queue.pop(0)			#List of states for the current stage
	next_stage=[]							#Set of states of next stage
	for state in states_list:
		next_states=find_all_next(state)
		for st_i1 in next_states:
			if st_i1 not in state_set:
				state_set.append(st_i1)		#Append to set of states if state is new
				min_cost.append((infinity,infinity))
			if st_i1 not in next_stage:
				next_stage.append(st_i1)	#New state in next stage
		#print("NS: ",next_stage)
		if state==s:						#Initial state
			#print("Begun")
			for i in range(1,len(next_states)+1):
				min_cost[i]=(0,0)			#First retrieval does not cost
		else:
			k=state[-1]						#Conveyor from which last car was retrieved
			current_car_colour=Conveyor[k-1][state[k-1]-1]
			cc=current_car_colour
			for st in next_states:
				i=state_set.index(st)
				j=state_set.index(state)
				if st[-1]==0:
					min_val=min(min_cost[i][0],min_cost[j][0])
					new_min=min_cost[j][0]
					if new_min<min_cost[i][0]:
						min_cost[i]=(new_min,j)

				k_next=st[-1]				#Conveyor from which next car is to be retrieved
				next_car_colour=Conveyor[k_next-1][st[k_next-1]-1]
				nc=next_car_colour
				
				if current_car_colour!=next_car_colour:
					min_val=min(min_cost[i][0],min_cost[j][0]+changeover_cost[cc-1][nc-1])
					new_min=min_cost[j][0]+changeover_cost[cc-1][nc-1]
					if new_min<min_cost[i][0]:
						min_cost[i]=(new_min,j)
				else:
					min_cost[i]=(min_cost[j][0],j)
	stage_queue.append(next_stage)
print(*list(zip(state_set,min_cost)),"\n")
print("MinCost: ",min_cost)

a=min_cost[-1]
path=[]
path.append(state_set[-1])
while a!=((0,-1)):
	path.append(state_set[a[1]])
	a=min_cost[a[1]]

print("Path: ",*path[::-1])
print("Cost: ",min_cost[-1][0])
end=time()
print("Run-time: ",end-start," seconds")