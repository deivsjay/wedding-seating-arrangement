'''
Divya Jagadeesh
CSCI 561
Spring 2017
Homework 2
'''

import re
import copy

# take input
def input():

    file = open("input.txt", "r")
    first_line = file.readline().rstrip('\n')
    first_line_list = re.sub("[^\w]", " ", first_line).split()
    num_of_attendees = int(first_line_list[0])
    num_of_tables = int(first_line_list[1])

    friends_and_enemies = []
    with file as infile:
        for line in infile:
            current_line = line.rstrip('\n')
            current_line_list = re.sub("[^\w]", " ", current_line).split()
            current_line_list[0] = int(current_line_list[0])
            current_line_list[1] = int(current_line_list[1])
            friends_and_enemies.append(current_line_list)

    return num_of_attendees, num_of_tables, friends_and_enemies

def cnf_clauses():
    num_of_attendees = input()[0]
    num_of_tables = input()[1]
    friends_and_enemies = input()[2]
    cnf = []

    # person should be at only 1 table
    for a in range(1, num_of_attendees + 1):
        sit_here_or_there = []
        for i in range(1, num_of_tables + 1):
            sit_here_or_there.append("X" + str(a) + "," + str(i))
        cnf.append(sit_here_or_there)
        for i in range(1, num_of_tables + 1):
            for j in range(i + 1, num_of_tables + 1):
                cant_sit_at_both = []
                cant_sit_at_both.append("~X" + str(a) + "," + str(i))
                cant_sit_at_both.append("~X" + str(a) + "," + str(j))
                cnf.append(cant_sit_at_both)

    # people who are friends or enemies
    for i in range(0, len(friends_and_enemies)):
        a = friends_and_enemies[i][0]
        b = friends_and_enemies[i][1]
        if friends_and_enemies[i][2] == 'E':
            for i in range(1, num_of_tables + 1):
                enemies = []
                enemies.append("~X" + str(a) + "," + str(i))
                enemies.append("~X" + str(b) + "," + str(i))
                cnf.append(enemies)
        else:
            for j in range(1, num_of_tables + 1):
                for k in range(1, num_of_tables + 1):
                    friends = []
                    if j != k:
                        friends.append("~X" + str(a) + "," + str(j))
                        friends.append("~X" + str(b) + "," + str(k))
                        cnf.append(friends)

    return cnf

def symbols():
    symbols = []
    num_of_attendees = input()[0]
    num_of_tables = input()[1]
    for i in range(1, num_of_attendees + 1):
        for j in range(1, num_of_tables + 1):
            positive_clause = "X" + str(i) + "," + str(j)
            negative_clause = "~X" + str(i) + "," + str(j)
            symbols.append(positive_clause)
            symbols.append(negative_clause)
    return symbols

def print_shit(my_shit):
    output_file = open('output.txt', 'w')
    for i in range(0, len(my_shit)):
        print >> output_file, my_shit[i]
    output_file.close()

def dpll_satisfiable():
    return new_dpll(cnf_clauses(), symbols(), {})

def decision_check(cnf, model):
    if len(cnf) == 0:
        output_if_true(model)
        return True
    for i in range(0, len(cnf)):
        if len(cnf[i]) == 0:
            return False
    return "no changes"

def new_dpll(cnf, symbols, model):

    # ends recursion
    decision = decision_check(cnf, model)
    if decision != "no changes":
        return decision

    # if pure symbol found, recurse
    pure_symbols = find_pure_symbol(symbols, cnf, model)
    if len(pure_symbols) > 0:
        for i in range(0, len(pure_symbols)):
            P1 = update2(pure_symbols[i], symbols, cnf, model, 1)
            P2 = update2(pure_symbols[i], symbols, cnf, model, 0)
            return new_dpll(P1[1], P1[0], P1[2]) or new_dpll(P2[1], P2[0], P2[2])

    # if unit clause is found, recurse
    unit_clauses = find_unit_clauses(symbols, cnf, model)
    if len(unit_clauses) > 0:
        for i in range(0, len(unit_clauses)):
            P1 = update2(unit_clauses[i], symbols, cnf, model, 1)
            P2 = update2(unit_clauses[i], symbols, cnf, model, 0)
            return new_dpll(P1[1], P1[0], P1[2]) or new_dpll(P2[1], P2[0], P2[2])

    if len(symbols) > 0:
        P1 = update2(symbols[0], symbols, cnf, model, 1)
        P2 = update2(symbols[0], symbols, cnf, model, 0)
        return new_dpll(P1[1], P1[0], P1[2]) or new_dpll(P2[1], P2[0], P2[2])

def update2(my_symbol, symbols, cnf, model, flag):

    # making sure what to assign random symbol
    if flag is 1:
        compliment_flag = 0
    else:
        compliment_flag = 1

    # find random symbol and compliment, update model
    model_copy = copy.deepcopy(model)
    model_copy[my_symbol] = flag
    if my_symbol[0] == 'X':
        my_compliment = "~" + my_symbol
    else:
        my_compliment = my_symbol[1:len(my_symbol)]
    model_copy[my_compliment] = compliment_flag

    # update symbols
    symbols_copy = copy.deepcopy(symbols)
    delete_these = []
    for i in range(0, len(symbols_copy)):
        if symbols_copy[i] == my_symbol:
            delete_these.append(i)
        if symbols_copy[i] == my_compliment:
            delete_these.append(i)
    temp_symbols_copy = []
    for i in range(0, len(symbols_copy)):
        if i not in delete_these:
            temp_symbols_copy.append(symbols_copy[i])
    symbols_copy = temp_symbols_copy

    # update cnf
    cnf_copy = copy.deepcopy(cnf)
    if flag == 1:
        positive_literal = my_symbol
        negative_literal = my_compliment
    else:
        negative_literal = my_symbol
        positive_literal = my_compliment
    delete_clauses = []
    for i in range(0, len(cnf_copy)):
        if positive_literal in cnf_copy[i]:
            delete_clauses.append(i)
    temp_cnf_copy = []
    for i in range(0, len(cnf_copy)):
        if i not in delete_clauses:
            temp_cnf_copy.append(cnf_copy[i])
    cnf_copy = temp_cnf_copy
    for i in range(0, len(cnf_copy)):
        if negative_literal in cnf_copy[i]:
            delete_literal = 100
            for j in range(0, len(cnf_copy[i])):
                if cnf_copy[i][j] == negative_literal:
                    delete_literal = j
            del cnf_copy[i][delete_literal]

    return symbols_copy, cnf_copy, model_copy


def find_pure_symbol(symbols, cnf, model):

    # find pure symbols
    pure_symbols = []
    for i in range(0, len(symbols)):
        found_symbol = False
        found_compliment = False
        for j in range(0, len(cnf)):
            if symbols[i][0] == 'X':
                if symbols[i] in cnf[j]:
                    found_symbol = True
                if "~" + symbols[i] in cnf[j]:
                    found_compliment = True
            else:
                if symbols[i] in cnf[j]:
                    found_symbol = True
                if symbols[i][1:len(symbols[i])] in cnf[j]:
                    found_compliment = True
        if found_symbol is True and found_compliment is False:
            pure_symbols.append(symbols[i])

    return pure_symbols

def find_unit_clauses(symbols, cnf, model):

    # find unit clause
    unit_clauses = []
    for i in range(0, len(cnf)):
        if len(cnf[i]) == 1:
            unit_clauses.append(cnf[i][0])

    return unit_clauses

def output_if_true(model):

    assignment_list = []
    model_copy = copy.deepcopy(model)
    for key in model_copy:
        if model_copy[key] == 1 and key[0] != "~":
            assignment_list.append(key)
    output_list = []
    output_list.append("yes")
    for i in range(0, len(assignment_list)):
        for j in range(0, len(assignment_list)):
            person = i + 1
            this_one = assignment_list[j].split(',')
            this_one[0] = this_one[0][1:len(this_one[0])]
            if int(this_one[0]) == person:
                output_list.append(this_one[0] + " " + this_one[1])
    # print_shit(assignment_list)
    print_shit(output_list)

def main():

    # print cnf_clauses()
    conclusion = dpll_satisfiable()
    if conclusion == False:
        output_file = open('output.txt', 'w')
        print >> output_file, "no"
        output_file.close()

if __name__ == "__main__":
    main()