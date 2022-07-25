# Network Shortest Path Solver

# --- Read Input ---

InputFile = 'inputnetwork.txt'
input_network = []


def read_input(input_file):
    """Reads the input.txt file and formats the problem"""

    # Open and read Input
    with open(input_file) as Prob:
        Prob = Prob.readlines()

    Count = 0
    for Line in Prob:
        Count += 1
        Line = Line.strip("\n")
        Line = Line.replace(" ", "")
        Line = Line.split(",")
        for n in Line:
            if not n.isnumeric():
                print("Please enter numeric input.")
                exit(1)
        if len(Line) != 2 * Count:
            print(
                "Please enter the correct input. There should be 2 values in the 1st line, 4 in the 2nd, 6 in the "
                "3rd, etc.")
            exit(1)
        Line = map(int, Line)
        Line = tuple(Line)
        input_network.append(Line)


read_input(InputFile)

# --- Optimal Decision and Value Table Creator ---

# Set variables needed for this section
NumStages = len(input_network)
NumPerStage = 2 ** NumStages
last_stage_cost = []
last_stage_directions = []
stage_cost = []
stage_directions = []
all_stage_cost = []
all_stage_directions = []

for j in range(0, len(input_network[-1]), 2):  # For every couple in the last input column
    # Checks cheapest way to each node and records direction and value
    if input_network[-1][j] < input_network[-1][j + 1]:
        cheap_cost = input_network[-1][j]
        direction = 'U'
    elif input_network[-1][j] > input_network[-1][j + 1]:
        cheap_cost = input_network[-1][j + 1]
        direction = 'D'
    else:
        cheap_cost = input_network[-1][j]
        direction = 'U or D'
    last_stage_cost.append(cheap_cost)
    last_stage_directions.append(direction)

all_stage_cost.append(last_stage_cost)
all_stage_directions.append(last_stage_directions)

for i in range(NumStages - 1):  # for the rest of the columns
    for j in range(0, len(input_network[-(i + 2)]), 2):
        # Checks cheapest way to each node and records direction and value
        if input_network[-(i + 2)][j] + last_stage_cost[int(j - 1 * (j / 2))] < input_network[-(i + 2)][j + 1] + \
                last_stage_cost[int(j + 1 - 1 * (j / 2))]:
            cheap_cost = input_network[-(i + 2)][j] + last_stage_cost[int(j - 1 * (j / 2))]
            direction = 'U'
        elif input_network[-(i + 2)][j] + last_stage_cost[int(j - 1 * (j / 2))] > input_network[-(i + 2)][j + 1] + \
                last_stage_cost[
                    int(j + 1 - 1 * (j / 2))]:
            cheap_cost = input_network[-(i + 2)][j + 1] + last_stage_cost[int(j + 1 - 1 * (j / 2))]
            direction = 'D'
        else:
            cheap_cost = input_network[-(i + 2)][j] + last_stage_cost[int(j - 1 * (j / 2))]
            direction = 'U or D'
        stage_cost.append(cheap_cost)
        stage_directions.append(direction)
    all_stage_cost.append(stage_cost)
    all_stage_directions.append(stage_directions)
    last_stage_cost = stage_cost
    last_stage_directions = stage_directions
    stage_cost = []
    stage_directions = []

min_cost = last_stage_cost[0]  # Sets the cost of the shortest route

# --- Shortest Path Determiner ---

# Set variables needed for this section
NumPath = 1
TotalNumPath = 1
PathsChecked = 0
temp_direction_count = 0
cheap_route = []
all_cheap_route = []
CheckingMulti = False

while NumPath > 0:  # Checks until all paths have been searched
    for i in range(len(all_stage_directions)):  # For each stage
        # Checks direction and sets index to follow shortest route
        temp_direction = all_stage_directions[-(i + 1)][temp_direction_count]
        if temp_direction == "U":
            temp_direction_count = temp_direction_count
        elif temp_direction == "D":
            temp_direction_count += 1
        elif temp_direction == "U or D":  # If either route is shortest adds another path to be checked
            TotalNumPath += 1
            NumPath += 1
            NumPath -= PathsChecked
            if (NumPath % 2) == 0:  # This means a different route will be searched
                temp_direction = "U"
            else:
                temp_direction = "D"
                temp_direction_count += 1
        else:
            print("Error in code")
            exit(1)
        cheap_route.append(temp_direction)
    temp_direction_count = 0
    NumPath -= 1
    PathsChecked += 1
    all_cheap_route.append(cheap_route)
    cheap_route = []

print("Shortest Path Found.")

# --- Table Created ---

NumX = len(all_stage_cost[0])
Headings = ["x"]
Footer = ["STAGE"]
Table = []

for i in range(NumStages):
    Headings.append(f"d{i} S{i}")
    Footer.append(f"{i}")

for i in range(NumStages):
    Row = []
    for j in range(NumX):
        try:
            if all_stage_directions[-(j + 1)][-(i + 1)].strip("") == "U or D":
                Row.append("U/D " + str(all_stage_cost[-(j + 1)][-(i + 1)]))
            else:
                Row.append(all_stage_directions[-(j + 1)][-(i + 1)] + "  " + str(all_stage_cost[-(j + 1)][-(i + 1)]))
        except IndexError:
            Row.append("")
    Table.append(Row)
Table.reverse()

for i in range(len(Table)):
    Table[i].insert(0, f"x{i + 1}")

Table.insert(0, Headings)
Table.append(Footer)


# --- .txt Files Created ---

def write_file(Filename, Text, Mode):
    """Writes to the a file"""

    # This structure allows a string, integer, float, list or list of lists to be written successfully
    with open(Filename, Mode) as f:
        if type(Text) is str or type(Text) is int or type(Text) is float:
            f.write(str(Text) + "\n")
        elif type(Text) is list:
            for item in Text:
                if type(item) is str:
                    f.write(str(item) + " ")
                elif type(item) is list:
                    f.write("\n")
                    for char in item:
                        f.write(str(f"{char}") + " \t")
    f.close()


# - Log.txt File Created -

write_file('lognetwork.txt', "This file shows the inner workings of the Network Cheapest Path Solver.\n", 'w')
write_file('lognetwork.txt',
           "The optimal decisions and associated values for a given stage and state are given in the table below: ",
           'a')
write_file('lognetwork.txt', Table, 'a')
write_file('lognetwork.txt', "\n", 'a')

if len(all_cheap_route) > 1:
    write_file('lognetwork.txt', "Multiple cheapest routes detected. \n", 'a')
    write_file('lognetwork.txt', "The cheapest routes are: \n", 'a')
    for i in range(len(all_cheap_route)):
        write_file('lognetwork.txt', all_cheap_route[i], 'a')
        write_file('lognetwork.txt', "\n", 'a')
else:
    write_file('lognetwork.txt', "The cheapest route is", 'a')
    write_file('lognetwork.txt', all_cheap_route[0], 'a')

write_file('lognetwork.txt', "\nThe cheapest route cost: ", 'a')
write_file('lognetwork.txt', min_cost, 'a')

# - Solution.txt File Created -

write_file('solutionnetwork.txt', "This file shows the output of the Network Cheapest Path Solver.\n", 'w')

if len(all_cheap_route) > 1:
    write_file('solutionnetwork.txt', "The cheapest routes are: \n", 'a')
    for i in range(len(all_cheap_route)):
        write_file('solutionnetwork.txt', all_cheap_route[i], 'a')
        write_file('solutionnetwork.txt', "\n", 'a')
else:
    write_file('solutionnetwork.txt', "The cheapest route is:", 'a')
    write_file('solutionnetwork.txt', all_cheap_route[0], 'a')

write_file('solutionnetwork.txt', "The cheapest route cost: ", 'a')
write_file('solutionnetwork.txt', min_cost, 'a')
