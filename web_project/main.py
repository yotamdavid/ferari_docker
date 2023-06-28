data = [1, 1, 2, 5, 8, 13, 21]
num = int(input("הכנס מספר: "))

for i in data:
    if i < num:
        print(i)
#בשורה אחת למטה
#print([i for i in [1, 1, 2, 5, 8, 13, 21] if i < int(input("הכנס מספר: "))])

#משימה 2
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
def find_common_elements(a, b):
    set_a = set(a)
    set_b = set(b)
    common_elements = list(set_a.intersection(set_b))
    return common_elements

print(find_common_elements(a, b))

#משימה 3
def remove_duplicates(lst):
    return list(set(lst))
original_list = [1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9]
new_list = remove_duplicates(original_list)
print(new_list)
