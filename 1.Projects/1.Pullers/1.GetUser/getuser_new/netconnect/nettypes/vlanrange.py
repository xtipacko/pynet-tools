#old version
# to-do: remove: duplicates like this 3,11: 1-12, 3, 11, 122-124, 127-128, 953 
#        fix:    add doesn't work with VlanRange type (unhide self.__ranges and use it to merge with...)
#        add:    support for + and - operators

import re

class VlanRange:
    digits = set('0123456789')
    delimiters = {',', '-'}
    space = {' '}
    allowedchars = digits | delimiters | space # | - is union
    
    def __init__(self, content):
        '''checks syntax for correctness, orders and unifies it'''
        self.__ranges = []
        rangelist = self.__parse_rangestr(content)
        self.add(*rangelist) # converts and merges ranges to self.__ranges, if needed
        
    def correct_syntax(self, content):
        if content == '':
            return content
        content = re.sub(r'\s+', ' ', content).strip() #removes extra spaces  
        content = re.sub(r'\s?,\s?', ',', content)
        content = re.sub(r'\s?-\s?', '-', content)
        correctexample = 'correct example: "111, 125-299, 3011, 3026"'
        if content[0] in VlanRange.delimiters:
            raise ValueError(f'Invalid VlanRange format (start from delimiter): {content!s}, {correctexample!s}')
        
        if any((char not in VlanRange.allowedchars) for char in content): #checks if it has invalid character
            raise ValueError(f'Invalid VlanRange format (invalid character): "{content}", {correctexample}')

        if re.search(r'\d\s\d|\d[,-]{2,}\d|-\d+-\d+', content):
            raise ValueError(f'Invalid VlanRange format: "{content}", {correctexample}')
        return content


    def __parse_rangestr(self, content):

        def parse_vlan(vlan):
            start = int(vlan)
            end = start+1 #wanna inclusive ranges
            if not 0 < start < 4095:
                raise ValueError(f'Vlan number {start} is not allowed')
            return range(start, end)

        def parse_range(rng):
            start, end = tuple(rng.split('-'))
            start, end = int(start), int(end)
            if start > end:
                start, end = end, start
            if (not 1 <= start <= 4094 or 
                not 1 <= end <= 4094):
                raise ValueError(f'Vlan number {start} is not allowed')
            end += 1 #wanna inclusive ranges
            return range(start, end)
        ranges = []
        if len(content) > 0:
            content = self.correct_syntax(content)
            strranges = content.split(',')        
            for rng in strranges: 
                if '-' not in rng:                
                    ranges.append(parse_vlan(rng))
                else:
                    ranges.append(parse_range(rng))         
        return ranges
    

    def __mergewithrange(self, mergingrange): # seeks for intersecting or neighbouring range in self.__ranges, and merges it with mergingrange (only for ranges)
        mr = mergingrange
        if (not 1 <= mr[0]  <= 4094 or 
            not 1 <= mr[-1] <= 4094):
            raise ValueError(f'Incorrect vlan numbers in range {mr[0]}-{mr[-1]} is not allowed')
        i=0
        while i < len(self.__ranges):
            rng = self.__ranges[i]
            if ((mr[0]-1 in rng or mr[0] in rng) and 
               not mr[-1] in rng): #mergingrange higher intersect or neighbour
                mr = range(rng[0], mr[-1]+1)
                self.__ranges.pop(i)
            elif ((mr[-1]+1 in rng or mr[-1] in rng) and 
                 not mr[0] in rng): #mergingrange lower intersect or neighbour
                mr = range(mr[0], rng[-1]+1)
                self.__ranges.pop(i)
            elif (rng[0] in mr and rng[-1] in mr):
                self.__ranges.pop(i)
            else:
                i+=1
        self.__ranges.append(mr)



    def add(self, *args):
        for arg in args:
            if type(arg) == range:
                self.__mergewithrange(arg)
            elif type(arg) == str:
                rangelist = self.__parse_rangestr(arg)
                self.add(*rangelist)
            elif type(arg) == int:
                self.add(*self.__parse_rangestr(str(arg)))
    

    def __substractrange(self, subtrahendrange): # seeks for intersecting ranges in self.__ranges, and substracting from them subtrahend range (only for ranges)
        sr = subtrahendrange
        i=0        
        while i < len(self.__ranges):
            rng  = self.__ranges[i]
            if rng[0] in sr and rng[-1] in sr:
                self.__ranges.pop(i)
                continue
            elif rng[0] in sr and rng[-1] not in sr:
                self.__ranges[i] = range(sr[-1]+1, rng[-1]+1)
            elif rng[0] not in sr and rng[-1] in sr:
                self.__ranges[i] = range(rng[0], sr[0])
            elif sr[0] in rng and sr[-1] in rng:
                range1 = range(rng[0],sr[0])
                range2 = range(sr[-1]+1,rng[-1]+1)
                self.__ranges[i] = range1
                self.__ranges.insert(i+1, range2)
                i+=1
            i+=1
       

    def remove(self, *args):
        for arg in args:
            if self & arg: #if it intersects
                if type(arg) == range:
                    self.__substractrange(arg)                      
                if type(arg) == str:
                    rangelist = self.__parse_rangestr(arg)
                    self.remove(*rangelist)                    
                if type(arg) == int:                
                    self.__substractrange(range(arg,arg+1))


    def __and__(self, other):
        if type(other) == range:
            r = other
            for rng in self.__ranges:
                if any([r[0] in rng,
                       r[-1] in rng,
                       rng[0] in r,
                       rng[-1] in r]):
                    return True
            return False
        elif type(other) == str:
            rangelist = self.__parse_rangestr(other)
            return any([self & rng for rng in rangelist])
        elif type(other) == VlanRange:
            return self & str(other)
        elif type(other) == int:
            return self & str(other)



    def __contains__(self, item):
        if type(item) == range:
            r = item
            for rng in self.__ranges:
                if r[0] in rng and r[-1] in rng:
                    return True
                elif r[0] in rng and r[-1] not in rng:
                    r = range(rng[0], r[0])
                    continue
                elif r[0] not in rng and r[-1] in rng:
                    r = range(r[-1]+1, rng[-1]+1)
                    continue
            return False
        elif type(item) == str:
            rangelist = self.__parse_rangestr(item)
            return all([rng in self for rng in rangelist])
        elif type(item) == int:
            return str(item) in self
    
    def sort(self):
        first = lambda rng: rng[0]
        self.__ranges.sort(key=first)

    def __str__(self): # returns ordered vlan range in str
        self.sort()
        result = []
        for rng in self.__ranges:
            if rng[0] == rng[-1]:
                result.append(str(rng[0]))
            else:
                result.append(f'{rng[0]!s}-{rng[-1]!s}')
        return ', '.join(result)


# if __name__ == '__main__':
#     debug = False
#     r = VlanRange('125,126,127, 124-128, 300-400, 500-600')
#     print('adding')
#     debug = True
#     r.remove('9000-10000')
#     print(r)
