import numpy as np

def find_possible_numbers(grid, row, col):
    """返回某个单元格可以填入的所有可能数字"""
    if grid[row, col] != 0:
        return []
    
    possible = set(range(1, 10))
    
    # 去除所在行、列已存在的数字
    possible -= set(grid[row, :])
    possible -= set(grid[:, col])
    
    # 去除所在 3x3 宫格已存在的数字
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    possible -= set(grid[start_row:start_row+3, start_col:start_col+3].flatten())
    
    return list(possible)

def lastRemainingCellInference(grid):
    """使用 Last Remaining Cell 策略推理确定的值，返回确定的单元格集合"""
    candidates = np.zeros((9, 9, 9), dtype=int)
    determined_values_set = set()  # 使用集合避免重复记录
    
    # 计算每个空格的初始候选数集
    for i in range(9):
        for j in range(9):
            if grid[i, j] == 0:
                possible = find_possible_numbers(grid, i, j)
                for num in possible:
                    candidates[i, j, num - 1] = 1
    
    # 遍历所有数字 1-9，检查 Last Remaining Cell 规则
    for num in range(1, 10):
        for i in range(9):
            # 检查行
            row_positions = [(i, j) for j in range(9) if candidates[i, j, num - 1] == 1]
            if len(row_positions) == 1:
                row, col = row_positions[0]
                if (row, col, num) not in determined_values_set:  # 检查是否已经记录过该位置
                    grid[row, col] = num
                    determined_values_set.add((row, col, num))  # 记录已填充的单元格
                
            # 检查列
            col_positions = [(j, i) for j in range(9) if candidates[j, i, num - 1] == 1]
            if len(col_positions) == 1:
                row, col = col_positions[0]
                if (row, col, num) not in determined_values_set:
                    grid[row, col] = num
                    determined_values_set.add((row, col, num))
        
        # 检查 3x3 宫格
        for box_row in range(3):
            for box_col in range(3):
                positions = []
                for i in range(3):
                    for j in range(3):
                        row, col = box_row * 3 + i, box_col * 3 + j
                        if candidates[row, col, num - 1] == 1:
                            positions.append((row, col))
                if len(positions) == 1:
                    row, col = positions[0]
                    if (row, col, num) not in determined_values_set:
                        grid[row, col] = num
                        determined_values_set.add((row, col, num))
    
    # 返回所有确定的单元格（行, 列, 数字）
    return list(determined_values_set)

def possible_number(grid):
    """返回每个空单元格的所有可能数字集合"""
    possible_numbers_grid = np.zeros((9, 9), dtype=object)  # 用于存储每个格子的候选数字集合
    
    for i in range(9):
        for j in range(9):
            if grid[i, j] == 0:  # 如果该格为空格
                possible_numbers_grid[i, j] = find_possible_numbers(grid, i, j)  # 计算并存储候选数字
                
    return possible_numbers_grid


# 示例数独（0 表示空白格）
sudoku_grid = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

# 计算确定的值
determined_values = lastRemainingCellInference(sudoku_grid)
print(determined_values)  

#测试一下possiblenumber策略

# 获取每个空单元格的所有可能数字
possible_numbers_grid = possible_number(sudoku_grid)

# 打印每个格子的候选数字
for i in range(9):
    for j in range(9):
        if possible_numbers_grid[i, j]:
            print(f"Cell ({i}, {j}) can have the following possible numbers: {possible_numbers_grid[i, j]}")