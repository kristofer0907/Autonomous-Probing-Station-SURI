class Test_shit:


    def count_zeros_in_float(self,number):
        number_str = str(number)

        # Initialize a counter for zeros
        zeros_count = 0

        # Iterate over each character in the string
        for char in number_str:
            if char == '0':
                zeros_count += 1

        return zeros_count
    
    def get_zeros(self,min,max,count=0 ):
        min = abs(min)
        
        
        min = str(min)
        if min[count]=="0" and min[count].isdigit()== True:
            count += 1
            return self.get_zeros(float(min),max,count)
    
        else:
            self.zeros = count
            print(self.zeros)

tester= Test_shit()
print(tester.count_zeros_in_float(-0.005))
print(tester.get_zeros(-0.005,0.005))