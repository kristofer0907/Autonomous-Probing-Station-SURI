def create_interval(start, end, step,zeros):
    
        interval_list = []
        num = start
        while round(num,zeros) <= end:
            interval_list.append(round(num,zeros))
            num += step
        return interval_list


def count_zeros_in_float(number):
        number_str = str(number)

        # Initialize a counter for zeros
        zeros_count = 0

        # Iterate over each character in the string
        for char in number_str:
            if char == '0':
                zeros_count += 1
        zerosa = zeros_count+1
        return zerosa+1




zeros = count_zeros_in_float(-0.1)
print(zeros)
a = (create_interval(-1,1,0.1,zeros))
print(a)