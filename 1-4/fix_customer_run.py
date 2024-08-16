from simulator import Simulator, EndCondition

mean_interarrival = float(input("Enter mean_interarrival: ")) # 1 minues in Book
mean_service = float(input("Enter mean_service: ")) # 0.5 minutes in Book
num_delays_required = int(input("Enter num_delays_required: ")) # 1000 in Book

print(f"\n\nSingle-server queueing system")
print(f"Mean interarrival time { mean_interarrival } minutes")
print(f"Mean service time { mean_service } minutes")
print(f"Number of customers { num_delays_required }")

# Make new instance of simulator with provided parameter
sim = Simulator(
    q_limit = 100,
    mean_interarrival = mean_interarrival,
    mean_service = mean_service,
    end_condition=num_delays_required,
    end_condition_type=EndCondition.FixCustomer
)

sim.run()
    
    