import matplotlib.pyplot as plt
import numpy as np
import csv, re, sys

def parse_file(name, number):

    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def nextTen(arr, ind):
        for i in range(0, 10):
            if (arr[ind + i]) == 0:
                return False
        return True

    def point_two_travel(travel, load):
        closest = find_nearest(travel, 0.2)
        index = travel.index(closest)
        load_at_closest = load[index]
        return load_at_closest

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
                if nextTen(loads, i):
                    first_nonzero_idx = i
                    break

        non_zero_load_subset = loads[first_nonzero_idx:] # Y axis of graph
        steps = [] # X Axis of graph
        for i in range(0, len(non_zero_load_subset)):
            steps.append(i * step_per_point)

        avg = point_two_travel(steps, non_zero_load_subset)
        if avg > highest_avg[0]:
            highest_avg[0] = avg
            highest_avg[1] = number
        elif avg < lowest_avg[0]:
            lowest_avg[0] = avg
            lowest_avg[1] = number

        return number, steps, non_zero_load_subset

def plot_test(name):
    global highest_avg
    highest_avg = [0, 0]
    global lowest_avg
    lowest_avg = [sys.float_info.max, 0]
    # name -> 2_5_S_2
    numbers = []
    x_axes = []
    y_axes = []

    test = 0
    for i in range(1, 50):
        try:
            regex = r"(\d+\_\d+)_(\D+)_(\d+)"
            spl = re.search(regex, name)
            grip_length = spl.group(1)
            grip_type = spl.group(2)
            tube_num = spl.group(3)

            first_dir = grip_length + "_" + grip_type
            second_dir = grip_type + "_" + tube_num
            filename = "csvs/" + first_dir + "/" + second_dir + "/" + name + "_" + str(i) + ".log"
            ret = parse_file(filename, i)
            numbers.append(ret[0])
            x_axes.append(ret[1])
            y_axes.append(ret[2])
            test += 1
        except FileNotFoundError as e:
            #print (e)
            pass

    index_hi = numbers.index(highest_avg[1])
    index_lo = numbers.index(lowest_avg[1])
    numbers.append(numbers[index_hi])
    numbers.append(numbers[index_lo])
    x_axes.append(x_axes[index_hi])
    x_axes.append(x_axes[index_lo])
    y_axes.append(y_axes[index_hi])
    y_axes.append(y_axes[index_lo])

    for i in range(0, len(numbers)):
        if numbers[i] == highest_avg[1]:
            color = "#FFC000"
            linewidth = 2.75
        elif numbers[i] == lowest_avg[1]:
            color = "#39C2D7"
            linewidth = 2.75
        else:
            color = "#dbdad6" # Dark gray
            linewidth = 1.0
        plt.plot(x_axes[i], y_axes[i], linewidth=linewidth, label=str(numbers[i]), color=color)

    print ("Found ", test, " tests")

if __name__ == "__main__":
    name = "2_5_S_2"
    plot_test(name)

    plt.title(name)
    plt.xlabel("Travel (mm)")
    plt.ylabel("Load (N)")

    plt.show()
