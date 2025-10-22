import os
import Moduls.defs as f

history = os.listdir("eredmenyek")

plus_file_name = "Finish_file.txt"
if plus_file_name in history:
    i = 0
    for file_name in history:
        if file_name == plus_file_name:
            del history[i]

    i += 1


matrix = []

for file_name in history:
    step = 0
    data = ["", "", ""]
    #csapat = data[0]; szint = data[1]; count = data[2]

    for e in file_name:
        if e == "_":
            step += 1

        elif e == ".":
            break

        else:
            data[step] += e

    data[1] = int(data[1])
    data[2] = int(data[2])

    matrix.append(data)

file = open(rf"eredmenyek/{plus_file_name}", "w", encoding="UTF-8")

csapatok = []

for e in matrix:
    if e[0] not in csapatok:
        csapatok.append(e[0])


for cs in csapatok:
    file.write(f"{cs}:\n")
    cs_sum = 0

    for i in range(1,5):
        file.write(f"-{i}.szint:")
        level_sum = 0

        num_l = []
        for e in matrix:  
            if e[0] == cs and e[1] == i:
                num_l.append(e[2])

        valid_start = 1
        valid_num = 3

        if len(num_l) == 0:
            valid_start = None

        elif len(num_l) > 3:
            valid_start = f.maximum(num_l) - 2

        else:
            valid_num = len(num_l)

        
        if valid_start != None:
            for j in range(valid_num):

                if i < 3:
                    mult = 1

                else:
                    mult = 2

                second_score = None

                with open(rf"eredmenyek/{cs}_{i}_{valid_start+j}.txt", "r", encoding="UTF-8") as fi:
                    lines = fi.readlines()
                    for line in lines:
                        if line.startswith("Idő:"):
                            time = ""

                            add = False
                            for chart in line:
                                if add:
                                    time += chart
                                if chart == ":":
                                    add = True

                            time = int(time)

                            file.write(f"\n\tprobálkozás-{valid_start+j}.: Idő:{time}")

                        elif line.startswith("Pont"):
                            score = ""

                            add = False
                            for chart in line:
                                if add:
                                    score += chart
                                if chart == ":":
                                    add = True

                            score = int(score)

                            file.write(f"\t Pont: {score}")

                        elif line.startswith("Felr"):
                            second_score = score*15*mult

                            file.write(f"\tFelrobbant.")

                    if second_score == None:
                        second_score = score*30*mult+time

                        file.write(f"\tHatástalanítva.\t")

                    file.write(f" -> Elért pont: {second_score}")

                    level_sum += second_score

        else:
            file.write(" Nincs adat")

        file.write(f"\n\n\t{i}.sz. össz.: {level_sum}\n\n")
        
        cs_sum += level_sum
    
    file.write(f"\n{cs} összesen {cs_sum} pontot ért el.\n\t----------------------------------------------------------------\n")