import sys
sys.stdin=open('/home/mukund/Competitive Coding/input.txt','r')
sys.stdout=open('/home/mukund/Competitive Coding/output.txt','w')

from time import time
start=time()

#GC instance
N=[2,2]

C=[[1,2],[1,3]]
changeover_cost=[[0,3,2],[4,0,3],[5,4,0]]
Conveyor=[[1,2],[1,3]]	#First element at each conveyor retrievable

no_of_conveyors=len(Conveyor)
no_of_colours=len(changeover_cost)
gamma=2

min_cost=[]									#DP Array

stage_queue=[]								#To load next stage with its states into algo
state_set=[]								#List of all states
infinity=1000000							#Infinity



def no_of_cars(colour,conveyor_index):
	count=0
	for i in Conveyor[conveyor_index]:
		if i==colour:
			count+=1
	return count

def findmin(colour,k):
	minimum=infinity
	for conv in range(no_of_conveyors):
		if conv!=k:
			for car_colour in Conveyor[conv]:
				minimum=min(minimum,changeover_cost[car_colour-1][colour-1])
	return minimum

def better_lb():
	maxbound=0;
	basic=gamma*(no_of_colours-1)
	for k in range(no_of_conveyors):
		mincost_sum=0
		for i in C[k]:
			if no_of_cars(i,k)>1:
				B=Conveyor[k][1:]
				for j in range(len(B)):
					mincost=changeover_cost[Conveyor[k][j]-1][Conveyor[k][j+1]-1]
					other_min=findmin(B[j],k)
					mincost_sum+=min(mincost,other_min)
		maxbound=max(maxbound,basic+mincost_sum)
	return maxbound


def ABH(sigma):
	UB=infinity
	lbB=better_lb()
	print("ABHLBB: ",lbB)
	stageQueue=[]
	s=[0 for x in range(no_of_conveyors+1)]		#Initial dummy state
	stage=[]
	stage.append(s)
	stageQueue.append(stage)
	stateSet=[s]
	minCost=[(0,-1)]
	upBnd=[0]
	es=[lbB]
	lb=[0]
	print(stageQueue)

	for stageIter in range(sum(N)+1):
		statesList=stageQueue.pop(0)			#List of states for the current stage
		nextStage=[]							#Set of states of next stage
		mv=infinity
		for state in statesList:
			next_states=find_all_next(state)
			for st_i1 in next_states:
				if st_i1 not in stateSet:
					stateSet.append(st_i1)		#Append to set of states if state is new
					minCost.append((infinity,infinity))
					upBnd.append(infinity)
					es.append(infinity)
					lb.append(infinity)
				if st_i1 not in nextStage:
					nextStage.append(st_i1)	#New state in next stage
	
			if state==s:						#Initial state
				for i in range(1,len(next_states)+1):
					minCost[i]=(0,0)			#First retrieval does not cost
					lb[i]=lbB
					upBnd[i]=0
					es[i]=lb[i]
			else:
				k=state[-1]						#Conveyor from which last car was retrieved
				cc=Conveyor[k-1][state[k-1]-1]	#Current car colour

				for st in next_states:
					i=stateSet.index(st)
					j=stateSet.index(state)
					if st[-1]==0:					#Final state
						min_val=min(minCost[i][0],minCost[j][0])
						new_min=minCost[j][0]
						if new_min<minCost[i][0]:
							minCost[i]=(new_min,j)
						lb[i]=0
						es[i]=0
						upBnd[i]=0

					else:							#Not the final state
						k_next=st[-1]				#Conveyor from which next car is to be retrieved
						nc=Conveyor[k_next-1][st[k_next-1]-1]	#Colour of next car

						#Minimum cost of next states
						if cc!=nc:
							min_val=min(minCost[i][0],minCost[j][0]+changeover_cost[cc-1][nc-1])
							new_min=minCost[j][0]+changeover_cost[cc-1][nc-1]
							if new_min<minCost[i][0]:
								minCost[i]=(new_min,j)
						else:
							minCost[i]=(minCost[j][0],j)

						upBnd[i]=min(upBnd[i],changeover_cost[cc-1][nc-1]+upBnd[j])
						lb[i]=min(lb[i],changeover_cost[cc-1][nc-1]+lbB)
						es[i]=lb[i]+minCost[i][0]
						if es[i]<mv:
							mv=es[i]
		
		for state in nextStage:
			if state!=s:
				i=stateSet.index(state)
				if minCost[i][0]+upBnd[i]<UB:
					UB=minCost[i][0]+upBnd[i]
				if es[i]>mv+(gamma*sigma):
					ix=nextStage.index(state)
					nextStage.pop(ix)
		stageQueue.append(nextStage)
		print("UBB: ",upBnd)
	print("LowerBound: ",list(zip(stateSet,lb)))
	print("E(S): ",es)
	print("UpperBound: ",upBnd)
	return UB


			


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
	elif sum(N)==sum(state[:len(state)-1]) and state[-1]!=0:
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

print(state_set)
lbb=better_lb()
E=[lbb]
up_bnd=[0]

#DP Procedure
ub=ABH(10)
print("Upd: ",ub)
for stage_iter in range(sum(N)+1):
	states_list=stage_queue.pop(0)			#List of states for the current stage
	next_stage=[]							#Set of states of next stage
	for state in states_list:
		print("Current: ",state)
		next_states=find_all_next(state)
		print("NSt: ",next_states)
		for st_i1 in next_states:
			if st_i1 not in state_set:
				state_set.append(st_i1)		#Append to set of states if state is new
				min_cost.append((infinity,infinity))
				E.append(infinity)
				up_bnd.append(infinity)
			if st_i1 not in next_stage:
				next_stage.append(st_i1)	#New state in next stage
		#print("NS: ",next_stage)
		print("SS: ",state_set)
		if state==s:						#Initial state
			#print("Begun")
			for i in range(1,len(next_states)+1):
				min_cost[i]=(0,0)			#First retrieval does not cost
		else:
			k=state[-1]						#Conveyor from which last car was retrieved
			current_car_colour=Conveyor[k-1][state[k-1]-1]
			cc=current_car_colour
			print("NSG: ",next_stage)
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
				
				#Find Minimum cost for the next states
				if current_car_colour!=next_car_colour:
					min_val=min(min_cost[i][0],min_cost[j][0]+changeover_cost[cc-1][nc-1])
					new_min=min_cost[j][0]+changeover_cost[cc-1][nc-1]
					if new_min<min_cost[i][0]:
						min_cost[i]=(new_min,j)
				else:
					min_cost[i]=(min_cost[j][0],j)

				up_bnd[i]=min(up_bnd[i],changeover_cost[cc-1][nc-1])
				
				lb=min_cost[i][0]+lbb
				E[i]=min_cost[i][0]+lbb
				print("E: ",E[i],"U: ",ub)
				if min_cost[i][0]+up_bnd[i]<ub and (min_cost[i][0]+up_bnd[i])>0:
					ub=min_cost[i][0]+up_bnd[i]
				if E[i]>=ub:
					print("Prune: ",st)
					ix=next_stage.index(st)
					next_stage.pop(ix)


	stage_queue.append(next_stage)

	print(min_cost,"\n")

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