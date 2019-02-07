import matplotlib.pyplot as plt
import csv

def parse_file(name):
    with open(name) as fil:
        # Strip first 5 lines
        date = fil.readline()
        units = fil.readline()
        reading_type = fil.readline()
        xaxis = fil.readline()
        travel_unit = fil.readline()

        csvreader = csv.DictReader(fil, delimiter="\t")
        reading_nums = []
        loads = []
        travels = []
        times = []
        for row in csvreader:
            reading_nums.append(int(row['Reading']))
            loads.append(float(row['Load']))
            travels.append(float(row['Travel']))
            times.append(float(row['Time']))


        num_readings = reading_nums[-1] # Total number of readings
        total_travel_dist = -1 * travels[-1] # Should be -2 for most
        step_per_point = total_travel_dist / num_readings # Avg step, x axis of graph

        first_nonzero_idx = 0
        # Find first non-zero load index
        for i in range(0, len(loads)):
            if loads[i] > 0: # First nonzero
                if loads[i+1] > 0: # Next number is also nonzero
                    first_nonzero_idx = i
                    break

        non_zero_load_subset = loads[first_nonzero_idx:] # Y axis of graph

        steps = [] # X Axis of graph
        for i in range(0, len(non_zero_load_subset)):
            steps.append(i * step_per_point)

        plt.plot(steps, non_zero_load_subset, linewidth=1.0)



if __name__ == "__main__":
    parse_file("csvs/2_5_S/S_2/2_5_S_2_1.log")
    parse_file("csvs/2_5_S/S_2/2_5_S_2_2.log")
    parse_file("csvs/2_5_S/S_2/2_5_S_2_3.log")

    plt.title("2_5_S_2")
    plt.xlabel("Travel (mm)")
    plt.ylabel("Load (N)")
    plt.show()
