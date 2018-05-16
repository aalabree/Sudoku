from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
####################
diagonal_units = [[x+y for x, y in zip(rows, cols)], [x+y for x, y in zip(rows, cols[::-1])]]


####################
# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist + diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)

peers = extract_peers(units, boxes)


def naked_twins(values):

    # First select boxes with 2 entries
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    # Collect boxes that have the same elements
    naked_twins = [[box1,box2] for box1 in potential_twins \
                    for box2 in peers[box1] \
                    if set(values[box1])==set(values[box2]) ]

    # For each pair of naked twins,
    for i in range(len(naked_twins)):
        box1 = naked_twins[i][0]
        box2 = naked_twins[i][1]
        # 1- compute intersection of peers
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        peers_int = peers1 & peers2
        # 2- Delete the two digits in naked twins from all common peers.
        for peer_val in peers_int:
            if len(values[peer_val])>2:
                for rm_val in values[box1]:
                    values = assign_value(values, peer_val, values[peer_val].replace(rm_val,''))
    return values



def eliminate(values):

    ##################################################################
    solved_values = []
    for box in values.keys():
        if (1 <= int(values[box]) <= 9):
            solved_values.append(box)
    print(solved_values)
    for x in solved_values:
        num = values[x]
        for peer in peers[x]:
            values[peer] = values[peer].replace(num,'')
            
    print (values)
    return values

    #raise NotImplementedError


def only_choice(values):

    ###################################################################
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    
   
    return values
    #raise NotImplementedError


def reduce_puzzle(values):

    ######################################################################
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    #raise NotImplementedError


def search(values):

    ###################################################################
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    #raise NotImplementedError


def solve(grid):
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')



