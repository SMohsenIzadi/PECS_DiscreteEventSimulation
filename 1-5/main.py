import os
from simulator import Simulator

initial_inv_level = 60
num_months = 120
num_policies = 9
num_values_demand = 4
mean_interdemand = 0.10
setup_cost = 32
incremental_cost = 3
holding_cost = 1
shortage_cost = 5.0
minlag = 0.5
maxlag = 1

prob_distrib_demand = [0, 0.167, 0.500, 0.833, 1.0]


print(f"Single-product inventory system")
print(f"Initial inventory level {initial_inv_level} items")
print(f"Number of demand sizes {num_values_demand}")
print(f"Distribution function of demand sizes  ")
prob_distrib = ""
for x in range(1, num_values_demand+1):
    prob_distrib += f"{prob_distrib_demand[x]}\t"
print(prob_distrib)
print(f"Mean interdemand time {mean_interdemand}", )
print(f"Delivery lag range {minlag} to {maxlag} months")
print(f"Length of the simulation {num_months} months")
print(f"K = {setup_cost}   i ={incremental_cost}   h ={holding_cost}   pi ={shortage_cost}")
print(f"Number of policies {num_policies}")


inv_list = [(0,0)]
with open(os.path.join(os.path.dirname(__file__), "inv.txt"), 'r') as inv_f:
    for line in inv_f:
        parts = line.strip().split()
        if len(parts) == 2:
            try:
                a = int(parts[0])
                b = int(parts[1])
                inv_list.append((a, b))
            except ValueError:
                print(f"Skipping line with non-integer values: {line.strip()}")
        else:
            print(f"Skipping line with unexpected format: {line.strip()}")

print(f"{str('Policy').rjust(8).ljust(8)}\t{str('total')}\t\t{str('ordering')}\t{str('holding')}\t\t{str('shortage')}")            

sim = Simulator(
        initial_inv_level=initial_inv_level,
        holding_cost=holding_cost,
        shortage_cost=shortage_cost,
        setup_cost=setup_cost,
        minlag=minlag,
        maxlag=maxlag,
        incremental_cost=incremental_cost,
        num_months=num_months,
        mean_interdemand=mean_interdemand,
        prob_distrib_demand=prob_distrib_demand
    )

for x in range(1, num_policies+1):
    (small, big) = inv_list[x]

    sim.load_policy(small, big)
    
    sim.run()

