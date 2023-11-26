data = [(1, 'A', '5'), (2, 'B', '4'), (3, 'C', '3'), (4, 'D', '2'), (5, 'E', '2'), (6, 'F', '3')]


grader_dict = {}
for i in data:
    grade, value = i[1],i[2]
    grader_dict[grade] = value
    
    
print(grader_dict)