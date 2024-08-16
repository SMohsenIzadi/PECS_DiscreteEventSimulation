from simulator import Simulator, EndCondition

mean_interarrival = float(input("Enter mean_interarrival: ")) # 1 minues in Book
mean_service = float(input("Enter mean_service: ")) # 0.5 minutes in Book
time_end = float(input("Enter time_end: ")) # 1000 in Book

print(f"\n\nSingle-server queueing system with fixed run length")
print(f"Mean interarrival time { mean_interarrival } minutes")
print(f"Mean service time { mean_service } minutes")
print(f"Length of the simulation { round(time_end ,3) } minutes")

# Make new instance of simulator with provided parameter
sim = Simulator(
    q_limit = 100,
    mean_interarrival = mean_interarrival,
    mean_service = mean_service,
    end_condition=time_end,
    end_condition_type=EndCondition.FixLength
)

sim.run()
    
    