# Capital Budgeting Solver

# --- Read Input ---

InputFile = 'inputcapbud.txt'
input_capbud_init = []


def read_input(input_file):
    """Reads the input.txt file and formats the problem"""

    # Open and read Input
    with open(input_file) as Prob:
        Prob = Prob.readlines()

    Count = 0
    for Line in Prob:
        Count += 1
        Line = Line.strip("\n")
        Line = Line.replace("(", "")
        Line = Line.replace(")", "")
        Line = Line.replace(" ", "")
        Line = Line.split(",")
        input_capbud_init.append(Line)


read_input(InputFile)

# --- Creates Initial Table ---

# Input added to table
init_table = {}
input_capbud = []

for i in range(len(input_capbud_init) - 1):
    input_capbud.append([i + 1])
    for j in range(int((len(input_capbud_init[i]) - 1) / 2)):
        plan = [input_capbud_init[i][(2 * j) + 1], input_capbud_init[i][(2 * j) + 2]]
        input_capbud[i].append(plan)

for i in range(len(input_capbud)):
    init_table[input_capbud[i][0]] = input_capbud[i][1:]

MaxCap = input_capbud_init[-1]
NumSub = len(input_capbud)
NumPlans = (max([len(i) for i in input_capbud_init]) - 1) / 2


# --- Solver Functions ---

# Finds the range of possible values for a given stage
def find_range(init_table, subsidiary_num, MaxCap=MaxCap):
    """Finds the range"""

    min_range = 0
    for i in range(1, subsidiary_num + 1):
        temp_range = []
        for j in init_table[i]:
            temp_range.append(j[0])
        min_range += int(min(temp_range[0]))

    try:
        cap_range = (int(min_range), int(MaxCap[0]))
    except TypeError:
        cap_range = (min_range, MaxCap)

    return cap_range

# Main solver
def plan_selector(init_table, NumStages=NumSub):
    """Solves the capital budgeting problem"""

    best_options = []
    best_options_final = []

    # Initial stage (stage 1)
    cap_range = find_range(init_table, 1)
    for cap in range(cap_range[0], cap_range[1] + 1):
        pot_options = []
        for plan in init_table[1]:
            if int(plan[0]) <= cap:
                pot_options.append(plan)
        best_op_val = max(pot_options, key=lambda x: int(x[1]))
        best_op = init_table[1].index(best_op_val)
        best_options.append([cap, best_op + 1, int(best_op_val[1])])
    stage_count = 2
    best_options_final.append(best_options)
    best_options = []

    # General stages (stage 1 + x)
    while stage_count != NumStages + 1:
        for cap in range(cap_range[0], cap_range[1] + 1):  # for capital
            temp_best_op_profit = 0
            temp_best_plan = []
            temp_best_op_profit_list = []
            temp_best_op = []
            multiple_best_op = False
            for plan in init_table[stage_count]:  # for each plan
                if int(plan[0]) <= cap:
                    rem_cap = cap - int(plan[0])  # calculate remaining capital
                for op in best_options_final[-1]:
                    if op[1] != 0:
                        if (op[0] <= rem_cap) and (
                                int(plan[1]) + op[2] >= temp_best_op_profit):  # if enough capital and more profitable
                            temp_best_op_profit = int(plan[1]) + op[2]
                            temp_best_op_profit_list.append([temp_best_op_profit, op[1], plan])
                            temp_best_plan = plan
            # The following Try-Except statements allow multiple best options
            try:
                max_prof = temp_best_op_profit_list[-1][0]
                temp_best_op = []
                for i in temp_best_op_profit_list:
                    if i[0] == max_prof:
                        temp_best_op.append(i[2])
                multiple_best_op = not all(op == temp_best_op[0] for op in temp_best_op)
            except IndexError:
                pass
            try:
                if multiple_best_op:
                    best_ops = []
                    plans = []
                    for i in temp_best_op:
                        if i not in plans:
                            plans.append(i)
                    for plan in plans:
                        best_ops.append(init_table[stage_count].index(plan) + 1)
                    best_options.append([cap, best_ops, temp_best_op_profit])
                else:
                    best_op = init_table[stage_count].index(temp_best_plan) + 1
                    best_options.append([cap, best_op, temp_best_op_profit])
            except ValueError:
                best_op = 0
                temp_best_op_profit = 0
                best_options.append([cap, best_op, temp_best_op_profit])
        stage_count += 1
        best_options_final.append(best_options)
        best_options = []
        rem_cap = 0

    return best_options_final


opt_values = plan_selector(init_table)

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
                    f.write(str(item))
                elif type(item) is list:
                    f.write("\n")
                    for char in item:
                        f.write(str(f"{char}") + "\t")
    f.close()


# --- Log.txt File Created ---

write_file('logcapbud.txt', "This file shows the inner workings of the Capital Budgeting Solver.\n", 'w')
write_file('logcapbud.txt',
           "The costs and returns for each plan are given in the table below: ",
           'a')

# -- Cost and Return Table --

# Headings for costs and returns table created
Headings_CR = [["Subsidiary:"], ["Plan Number:"]]
for i in range(NumSub):
    Headings_CR[0].append(f"{i + 1}\t")
for i in range(1, int(NumPlans) + 1):
    Headings_CR[1].append([f"c{i}j r{i}j"])

write_file('logcapbud.txt', Headings_CR, 'a')
write_file('logcapbud.txt', "\n", 'a')

# Formats the init_table dict to be writable
for i in range(int(NumPlans)):
    row = []
    row.append([f"{i + 1}\t\t"])
    for key in init_table.keys():
        try:
            row.append([init_table[key][i][0]])
            row.append(["     "])
            row.append([init_table[key][i][1]])
            row.append(["\t\t"])
        except IndexError:
            row.pop()
            row.append(["\t", "-", "     ", "-"])
            row.append(["\t\t"])
    for j in row:
        write_file('logcapbud.txt', j, 'a')
    write_file('logcapbud.txt', "\n", 'a')

# -- Forward Recursion Table --

# Headings for forward recursion table created
Headings_FR = [["X"]]
for i in range(1, int(NumSub) + 1):
    Headings_FR[0].append([f"d{i}(x) S{i}(x)"])

write_file('logcapbud.txt', "\nThe forward recursion table is below: ", 'a')
write_file('logcapbud.txt', Headings_FR, 'a')

test_region = find_range(init_table, 1, MaxCap)
# Formats the opt_values list to be writable
for i in range(len(range(test_region[0], test_region[1] + 1))):
    row = [range(test_region[0], test_region[1] + 1)[i]]
    for j in range(NumSub):
        if type(opt_values[j][i][1]) is list:
            row.append(f"{opt_values[j][i][1][0]}/{opt_values[j][i][1][1]}")
            row.append(opt_values[j][i][2])
        else:
            if opt_values[j][i][1] == 0:
                row.append("-")
            else:
                row.append(opt_values[j][i][1])
            if opt_values[j][i][2] == 0:
                row.append("-")
            else:
                row.append(opt_values[j][i][2])
    write_file('logcapbud.txt', [row], 'a')

# - Solution.txt File Created -

write_file('solutioncapbud.txt', "This file shows the output of the Capital Budgeting Solver.\n", 'w')
write_file('solutioncapbud.txt', f"The maximum return for {MaxCap[0]} units of capital is {opt_values[-1][-1][-1]}.\n",
           'a')

# Traces decision route
try: # Although unnecessary this try statement will solve the problem without giving the route to prevent errors
    decision_routes = []
    check_again = False
    NewCap = MaxCap
    # Makes initial decision
    NewCap = int(MaxCap[0]) - int(init_table[int(NumSub)][opt_values[-1][-1][1] - 1][0])
    decision_routes.append([opt_values[-1][-1][1] - 1][0] + 1)
    # Makes decisions for other stages
    for i in range(1, NumSub):
        try:
            decision_routes.append(opt_values[int(NumSub - 1) - i][NewCap - test_region[0]][1])
            NewCap = int(NewCap) - int(
                init_table[NumSub - i][opt_values[int(NumSub - 1) - i][NewCap - test_region[0]][1]-1][0])
        except TypeError:
            check_again = True
            decision_routes.pop()
            poss_options = (opt_values[int(NumSub - 1) - i][NewCap - test_region[0]][1])
            decision_routes.append([poss_options[0]][0])
            NewCap = int(NewCap) - int(init_table[NumSub - i][poss_options[0] - 1][0])

    # Traces 2nd decision route if another route is detected
    if check_again:
        NewCap = int(MaxCap[0]) - int(init_table[int(NumSub)][opt_values[-1][-1][1] - 1][0])
        decision_routes.append([opt_values[-1][-1][1] - 1][0] + 1)
        for i in range(1, NumSub):
            try:
                decision_routes.append(opt_values[int(NumSub - 1) - i][NewCap - test_region[0]][1])
                NewCap = int(NewCap) - int(
                    init_table[NumSub - i][opt_values[int(NumSub - 1) - i][NewCap - test_region[0]][1]-1][0])
            except TypeError:
                check_again = True
                decision_routes.pop()
                poss_options = (opt_values[int(NumSub - 1) - i][NewCap - test_region[0]][1])
                decision_routes.append([poss_options[1]][0])
                NewCap = int(NewCap) - int(init_table[NumSub - i][poss_options[1] - 1][0])
        decision_routes = [decision_routes[3:], decision_routes[:3]]
        write_file('solutioncapbud.txt', f"The decision routes are: {decision_routes}.\n", 'a')
    else:
        write_file('solutioncapbud.txt', f"The decision route is: {decision_routes}.\n", 'a')
except Exception:
     pass
