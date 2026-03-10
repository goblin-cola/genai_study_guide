
def printme(str):
    print(f'hi there {str}')

def looptest(str):
    for i, v in enumerate(str):
        print(f'{i}: {v}')

def looplist(lst):
    for i in range(len(lst)):
        print(f'{i}: {lst[i]}')

    for i, v in enumerate(lst):
        print(f'{i}: {v}')

def matrixloop():
    matrix = [[0, 1, 1, 0, 1],
              [1, 1, 0, 1, 0],
              [0, 1, 1, 1, 0],
              [1, 1, 1, 1, 0],
              [1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0]
    ]

    width = len(matrix[0])
    height = len(matrix)
    max_land = [[0 for _ in range(width)] for _ in range(height)]
    max_land_found = 0


    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == 0:
                max_land[i][j] = 0
                continue

            positions = []
            if i !=0 and j != 0:
                positions.append(max_land[i - 1][j])
                positions.append(max_land[i-1][j-1])
                positions.append(max_land[i][j-1])
            else:
                max_land[i][j] = 1
                continue

            min_above = min(positions)
            max_land[i][j] = min_above + 1
            max_land_found = max(max_land_found, max_land[i][j])

    max_area = max_land_found**2
    print(f'found max land: {max_land_found}, max area: {max_area}')
    return max_area


def isValidSubsequence(array, sequence):
    # subsequence is a dequence that can be dervied from another sequence
    # by deleting some elements without reordering the remaining elements

    idx = 0
    found = []

    for value in array:
        if idx == len(sequence):
            break

        if value == sequence[idx]:
            idx += 1

    return idx == len(sequence)




if __name__ == '__main__':
    #printme('user')
    #looptest('loopy user')
    #looplist([4, 6, 9])
    #matrixloop()
    isValidSubsequence([5, 1, 22, 25, 6, -1, 8, 10], [1, 6, -1, 10])