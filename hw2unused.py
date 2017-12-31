
# def pl_resolution():
#     cnf = cnf_clauses()
#     new = []
#     # while True:
#     for i in range(0, len(cnf)):
#         for j in range(0, len(cnf)):
#             if i != j:
#                 print "clause 1: %s" % cnf[i]
#                 print "clause 2: %s" % cnf[j]
#                 resolvants = pl_resolve(cnf[i], cnf[j])
#                 print "resolvants: %s" % resolvants
#                 if resolvants == []:
#                     return False
#                 elif resolvants != ["no changes"]:
#                     new.append(resolvants)
#                     temp_new = []
#                     indicies = []
#                     for a in range(0, len(new)):
#                         for b in range(0, len(new)):
#                             if a != b and new[a] == new[b]:
#                                 indicies.append(j)
#                     for a in range(0, len(new)):
#                         if a not in indicies:
#                             temp_new.append(new[a])
#                     new = temp_new
#     print "new: %s" % new
#     if len(new) == 0:
#         return True
#     found = True
#     for i in range(0, len(new)):
#         if new[i] not in cnf:
#             found = False
#     if found == True:
#         return True
#         # found = 0
#         # for j in range(0, len(cnf)):
#         #     if new[i] == cnf[j]:
#         #         found = 1
#         # if found == 0:
#         #     return True
#     for i in range(0, len(new)):
#         cnf.append(new[i])
#
#
# def pl_resolve(clause1, clause2):
#     clause1_index = -1
#     clause2_index = -1
#     compliment_flag = 0
#     for i in range(0, len(clause1)):
#         if clause1[i][0] == '~':
#             compare_clause = clause1[i][1:len(clause1[i])]
#         else:
#             compare_clause = "~" + clause1[i]
#         for j in range(0, len(clause2)):
#             if compliment_flag == 0 and clause2[j] == compare_clause:
#                 clause1_index = i
#                 clause2_index = j
#                 compliment_flag = 1
#             elif compliment_flag == 1 and clause2[j] == compare_clause:
#                 return ["no changes"]
#     resolution_statement = []
#     if compliment_flag == 1:
#         for i in range(0, len(clause1)):
#             if i != clause1_index and clause1[i] not in resolution_statement:
#                 resolution_statement.append(clause1[i])
#         for j in range(0, len(clause2)):
#             if j != clause2_index and clause2[j] not in resolution_statement:
#                 resolution_statement.append(clause2[j])
#         return resolution_statement
#     else:
#         return ["no changes"]

def update(my_symbol, symbols, cnf, model):

    # update model
    model[my_symbol] = 1
    if my_symbol[0] == 'X':
        my_compliment = "~" + my_symbol
    else:
        my_compliment = my_symbol[1:len(my_symbol)]
    model[my_compliment] = 0

    # update symbols
    delete_these = []
    for i in range(0, len(symbols)):
        if symbols[i] == my_symbol:
            delete_these.append(i)
        if symbols[i] == my_compliment:
            delete_these.append(i)
    temp_symbols = []
    for i in range(0, len(symbols)):
        if i not in delete_these:
            temp_symbols.append(symbols[i])
    symbols = temp_symbols

    # update cnf
    delete_clauses = []
    for i in range(0, len(cnf)):
        if my_symbol in cnf[i]:
            delete_clauses.append(i)
    temp_cnf = []
    for i in range(0, len(cnf)):
        if i not in delete_clauses:
            temp_cnf.append(cnf[i])
    cnf = temp_cnf
    for i in range(0, len(cnf)):
        if my_compliment in cnf[i]:
            delete_literal = 100
            for j in range(0, len(cnf[i])):
                if cnf[i][j] == my_compliment:
                    delete_literal = j
            del cnf[i][delete_literal]

    return symbols, cnf, model


def random_assigment(symbols, cnf, model, flag):

    # making sure what to assign random symbol
    if flag is 1:
        compliment_flag = 0
    else:
        compliment_flag = 1

    # find random symbol and compliment, update model
    my_symbol = symbols[0]
    model[my_symbol] = flag
    if my_symbol[0] == 'X':
        my_compliment = "~" + my_symbol
    else:
        my_compliment = my_symbol[1:len(my_symbol)]
    model[my_compliment] = compliment_flag

    # update symbols
    delete_these = []
    for i in range(0, len(symbols)):
        if symbols[i] == my_symbol:
            delete_these.append(i)
        if symbols[i] == my_compliment:
            delete_these.append(i)
    temp_symbols = []
    for i in range(0, len(symbols)):
        if i not in delete_these:
            temp_symbols.append(symbols[i])
    symbols = temp_symbols

    # update cnf
    if flag == 1:
        positive_literal = my_symbol
        negative_literal = my_compliment
    else:
        negative_literal = my_symbol
        positive_literal = my_compliment
    delete_clauses = []
    for i in range(0, len(cnf)):
        if positive_literal in cnf[i]:
            delete_clauses.append(i)
    temp_cnf = []
    for i in range(0, len(cnf)):
        if i not in delete_clauses:
            temp_cnf.append(cnf[i])
    cnf = temp_cnf
    for i in range(0, len(cnf)):
        if negative_literal in cnf[i]:
            delete_literal = 100
            for j in range(0, len(cnf[i])):
                if cnf[i][j] == negative_literal:
                    delete_literal = j
            del cnf[i][delete_literal]

    return symbols, cnf, model

    def new_find_unit_clause(symbols, cnf, model):

    # find unit clause
    unit_clause = ""
    for i in range(0, len(cnf)):
        if len(cnf[i]) == 1:
            unit_clause = cnf[i][0]
            break

    # if unit clause found
    if unit_clause != "":
        # update model
        model[unit_clause] = 1
        if unit_clause[0] == 'X':
            unit_compliment = "~" + unit_clause
        else:
            unit_compliment = unit_clause[1:len(unit_clause)]
        model[unit_compliment] = 0
        # update symbols
        delete_these = []
        for i in range(0, len(symbols)):
            if symbols[i] == unit_clause:
                delete_these.append(i)
            if symbols[i] == unit_compliment:
                delete_these.append(i)
        temp_symbols = []
        for i in range(0, len(symbols)):
            if i not in delete_these:
                temp_symbols.append(symbols[i])
        symbols = temp_symbols
        # update cnf
        delete_clauses = []
        for i in range(0, len(cnf)):
            if unit_clause in cnf[i]:
                delete_clauses.append(i)
        temp_cnf = []
        for i in range(0, len(cnf)):
            if i not in delete_clauses:
                temp_cnf.append(cnf[i])
        cnf = temp_cnf
        for i in range(0, len(cnf)):
            if unit_compliment in cnf[i]:
                delete_literal = 100
                for j in range(0, len(cnf[i])):
                    if cnf[i][j] == unit_compliment:
                        delete_literal = j
                del cnf[i][delete_literal]

    return unit_clause, symbols, cnf, model

    def new_find_pure_symbol(symbols, cnf, model):

    # print "symbols before going through find pure symbol: %s" % symbols
    # print "cnf before going through find pure symbol: %s" % cnf
    # print "model before going through find pure symbol: %s" % model

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

    my_symbol = "none"
    # if pure symbol found
    if len(pure_symbols) > 0:
        # update model
        my_symbol = pure_symbols[0]
        model[my_symbol] = 1
        if my_symbol[0] == 'X':
            my_compliment = "~" + my_symbol
        else:
            my_compliment = my_symbol[1:len(my_symbol)]
        model[my_compliment] = 0
        # update symbols
        delete_these = []
        for i in range(0, len(symbols)):
            if symbols[i] == my_symbol:
                delete_these.append(i)
            if symbols[i] == my_compliment:
                delete_these.append(i)
        temp_symbols = []
        for i in range(0, len(symbols)):
            if i not in delete_these:
                temp_symbols.append(symbols[i])
        symbols = temp_symbols
        # update cnf
        delete_clauses = []
        for i in range(0, len(cnf)):
            if my_symbol in cnf[i]:
                delete_clauses.append(i)
        temp_cnf = []
        for i in range(0, len(cnf)):
            if i not in delete_clauses:
                temp_cnf.append(cnf[i])
        cnf = temp_cnf
        for i in range(0, len(cnf)):
            if my_compliment in cnf[i]:
                delete_literal = 100
                for j in range(0, len(cnf[i])):
                    if cnf[i][j] == my_compliment:
                        delete_literal = j
                del cnf[i][delete_literal]

    # print "symbols AFTER going through find pure symbol: %s" % symbols
    # print "cnf AFTER going through find pure symbol: %s" % cnf
    # print "model AFTER going through find pure symbol: %s" % model

    return my_symbol, symbols, cnf, model



# def dpll(cnf, symbols, model):
#     if len(cnf) == 0:
#         return True
#     literal = False
#     for i in range(0, len(cnf)):
#         literal = False
#         false_literal = 0
#         for j in range(0, len(cnf[i])):
#             if cnf[i][j] in model:
#                 if model[cnf[i][j]] == 1:
#                     literal = True
#                     j = len(cnf[i])
#                 else:
#                     false_literal = false_literal + 1
#         if literal is False:
#             if false_literal == len(cnf[i]):
#                 return False
#             i = cnf[i]
#     if literal is True:
#         return True
#     returned = find_pure_symbol(cnf, symbols, model)
#     P = returned[0]
#     cnf = returned[1]
#     if len(P) > 0:
#         symbol_index = 0
#         compliment_index = 0
#         for i in range(0, len(symbols)):
#             if symbols[i] == P[0]:
#                 model[symbols[i]] = True
#                 symbol_index = i
#                 # if i % 2 == 0:
#                 if symbols[i][0] == 'X':
#                     for j in range(0, len(symbols)):
#                         if symbols[j] == "~" + symbols[i]:
#                             compliment_index = j
#                     model["~" + symbols[i]] = False
#                 else:
#                     for j in range(0, len(symbols)):
#                         if symbols[j] == symbols[i][1:len(symbols[i])]:
#                             compliment_index = j
#                     model[symbols[i][1:len(symbols[i])]] = False
#         temp_symbols = []
#         for i in range(0, len(symbols)):
#             if i != symbol_index and i != compliment_index:
#                 temp_symbols.append(symbols[i])
#         symbols = temp_symbols
#         return dpll(cnf, symbols, model)
#     # print "model after pure symbols: %s" % model
#     # print "symbols after pure symbols: %s" % symbols
#     returned = find_unit_clause(cnf, model)
#     P = returned[0]
#     cnf = returned[1]
#     if P != "":
#         symbol_index = 0
#         compliment_index = 0
#         for i in range(0, len(symbols)):
#             if symbols[i] == P:
#                 model[symbols[i]] = True
#                 symbol_index = i
#                 # if i % 2 == 0:
#                 if symbols[i][0] == 'X':
#                     for j in range(0, len(symbols)):
#                         if symbols[j] == "~" + symbols[i]:
#                             compliment_index = j
#                     model["~" + symbols[i]] = False
#                 else:
#                     for j in range(0, len(symbols)):
#                         if symbols[j] == symbols[i][1:len(symbols[i])]:
#                             compliment_index = j
#                     model[symbols[i][1:len(symbols[i])]] = False
#         temp_symbols = []
#         for i in range(0, len(symbols)):
#             if i != symbol_index and i != compliment_index:
#                 temp_symbols.append(symbols[i])
#         symbols = temp_symbols
#         return dpll(cnf, symbols, model)
#     # print "model after unit clause: %s" % model
#     # print "symbols after unit clause: %s" % symbols
#     print "symbols before if statement: %s" % symbols
#     if len(symbols) > 0:
#         print "symbols after if statement: %s" % symbols
#         "enters if statement after len symbols in dpll"
#         P = first(symbols)
#         rest = rest_of(symbols)
#         # print "symbols in dpll: %s" % symbols
#         return1 = update_symbols_and_model(symbols, model, P, True, cnf)
#         return2 = update_symbols_and_model(symbols, model, P, False, cnf)
#         symbols_return1 = return1[0]
#         model_return1 = return1[1]
#         cnf_return1 = return1[2]
#         symbols_return2 = return2[0]
#         model_return2 = return2[1]
#         cnf_return2 = return2[2]
#         return dpll(cnf_return1, symbols_return1, model_return1) \
#            or dpll(cnf_return2, symbols_return2, model_return2)

# def update_symbols_and_model(symbols, model, P, flag, cnf):
#     # print "entered update"
#     # print "P: %s" % P
#     # print "symbols in update: %s" % symbols
#     if flag is True:
#         compliment_flag = False
#     else:
#         compliment_flag = True
#     symbol_index = 0
#     compliment_index = 0
#     for i in range(0, len(symbols)):
#         if symbols[i] == P:
#             # print "entered if statement in update"
#             model[symbols[i]] = flag
#             symbol_index = i
#             # if i % 2 == 0:
#             if symbols[i][0] == 'X':
#                 for j in range(0, len(symbols)):
#                     if symbols[j] == "~" + symbols[i]:
#                         compliment_index = j
#                 model["~" + symbols[i]] = compliment_flag
#             else:
#                 for j in range(0, len(symbols)):
#                     if symbols[j] == symbols[i][1:len(symbols[i])]:
#                         compliment_index = j
#                 model[symbols[i][1:len(symbols[i])]] = compliment_flag
#     temp_symbols = []
#     for i in range(0, len(symbols)):
#         if i != symbol_index and i != compliment_index:
#             temp_symbols.append(symbols[i])
#     symbols = temp_symbols
#
#     delete_indicies = []
#     for key in model:
#         for i in range(0, len(cnf)):
#             if model[key] == 1 and key in cnf[i]:
#                 delete_indicies.append(i)
#     temp_cnf = []
#     for i in range(0, len(cnf)):
#         if i not in delete_indicies:
#             temp_cnf.append(cnf[i])
#     cnf = temp_cnf
#
#     # print "model in update function: %s" % model
#     return symbols, model, cnf

# def find_pure_symbol(cnf, symbols, model):
#     # print "entered pure symbols"
#     pure_symbols = []
#
#     for i in range(0, len(symbols)):
#         found_symbol = False
#         found_compliment = False
#         for j in range(0, len(cnf)):
#             # if i % 2 == 0:
#             if symbols[i][0] == 'X':
#                 if symbols[i] in cnf[j]:
#                     found_symbol = True
#                 if "~" + symbols[i] in cnf[j]:
#                     found_compliment = True
#             else:
#                 if symbols[i] in cnf[j]:
#                     found_symbol = True
#                 if symbols[i][1:len(symbols[i])] in cnf[j]:
#                     found_compliment = True
#         if found_symbol is True and found_compliment is False:
#             pure_symbols.append(symbols[i])
#     # print "pure symbols: %s" % pure_symbols
#     if len(pure_symbols) > 0:
#         delete_indicies = []
#         for i in range(0, len(cnf)):
#             if pure_symbols[0] in cnf[i]:
#                 delete_indicies.append(i)
#         temp_cnf = []
#         for i in range(0, len(cnf)):
#             if i not in delete_indicies:
#                 temp_cnf.append(cnf[i])
#         cnf = temp_cnf
#
#     return pure_symbols, cnf

# def find_unit_clause(cnf, model):
#     # print "entered unit clause: %s" % cnf
#     unit_clause = ""
#     for i in range(0, len(cnf)):
#         # print "entered for loop: %s" % cnf[i]
#         if len(cnf[i]) == 1 and cnf[i][0] not in model:
#             unit_clause = cnf[i][0]
#             del cnf[i]
#             break
#     return unit_clause, cnf



def first(symbols):
    print "in first function: %s" % symbols
    return symbols[0]



def rest_of(symbols):
    del symbols[0]
    return symbols

# commented out in input function:
    # print "first line: %s" % first_line_list
        # print "number of attendees: %s" % num_of_attendees
    # print "number of tables: %s" % num_of_tables
                # print "current line list: %s" % current_line_list
        # print "friends and enemies: %s" % friends_and_enemies

# commented out in cnf clauses: 

    # print "friends and enemies: %s" % friends_and_enemies
    # print "cnf: %s" % print_shit(cnf)

# deleted print statements and commented out in decision check:
        print "model in decision check: %s" % model

# deleted print statements and commented out in dpll

    # print "model: %s" % model
    # print "cnf: %s" % cnf
            # P = update(pure_symbols[i], symbols, cnf, model)
    # P = new_find_pure_symbol(symbols, cnf, model)
    # if P[0] != "none":
    #     return new_dpll(P[2], P[1], P[3])
            # P = update(unit_clauses[i], symbols, cnf, model)
    # P = new_find_unit_clause(symbols, cnf, model)
    # if P[0] != "":
    #     return new_dpll(P[2], P[1], P[3])

# deleted print statements and commented out in update2
    print "flag value: %s" % flag
    print "my symbol: %s" % my_symbol
        print "model before: %s" % model_copy
    print "my compliment: %s" % my_compliment

    print "model after: %s" % model_copy
        print "symbols before: %s" % symbols_copy
    print "symbols after: %s" % symbols_copy
    print "positive literal: %s" % positive_literal
    print "negative literal: %s" % negative_literal
    print "cnf before: %s" % cnf_copy
    print "cnf after: %s\n" % cnf_copy

# deleted print statements and commented out in main
    # print "hello"
    # print input()
    print "cnf clauses: "
    print_shit(cnf_clauses())
    print "number of cnf clauses: %s" % len(cnf_clauses())
    print "symbols: "
    print_shit(symbols())
    print "number of symbols: %s" % len(symbols())
    # print find_pure_symbol(cnf_clauses(), symbols(), {})
    # print find_unit_clause(cnf_clauses(), {})
    print "DPLL conclusion: %s" % conclusion
    # print "number of pure symbols: %s" % len(dpll(cnf_clauses(), symbols(), {}))
    # print "cnf clause first char should be ~: %s" % cnf_clauses()[1][1][0]
    # print "without ~: %s" % cnf_clauses()[1][1][1:len(cnf_clauses()[1][1])]
    # print "cnf with ~: %s" % "~" + cnf_clauses()[0][1][0:len(cnf_clauses()[0][1])]
    # print "cnf with ~ round 2: %s" % "~" + cnf_clauses()[0][1]
    # print pl_resolution()
    # print pl_resolve(['~X1,1'], ['X1,1', 'X3,1'])