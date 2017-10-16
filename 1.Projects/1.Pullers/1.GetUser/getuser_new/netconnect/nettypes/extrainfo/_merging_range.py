class A:
    def __init__(self, *args):
        self.ranges = [*args]

    def mergewithrange(self, mergingrange):
        for i, rng in enumerate(self.ranges):
            if (mergingrange[0]-1 in rng and #mergingrange higher intersect or neighbour
            not mergingrange[-1] in rng):
                self.ranges[i] = range(rng[0], mergingrange[-1]+1)
            elif (mergingrange[-1]+1 in rng and  #mergingrange lower intersect or neighbour
            not mergingrange[0] in rng):
                self.ranges[i] = range(mergingrange[0], rng[-1]+1)

print('--0 no')
a = A(range(30,101))

a.mergewithrange(range(5,20))

for rng in a.ranges:
    print(rng)

print('--1 no')
a = A(range(30,101))

a.mergewithrange(range(130,150))

for rng in a.ranges:
    print(rng)

print('--2 merge intersect lower')
a = A(range(30,101))

a.mergewithrange(range(10,50))

for rng in a.ranges:
    print(rng)

print('--3 merge neighbour lower')
a = A(range(30,101))

a.mergewithrange(range(5,30))

for rng in a.ranges:
    print(rng)

print('--4 merge intersect higher')
a = A(range(30,101))

a.mergewithrange(range(50,150))

for rng in a.ranges:
    print(rng)

print('--5 merge neighbour higher ')
a = A(range(30,101))

a.mergewithrange(range(101,150))

for rng in a.ranges:
    print(rng)

print('--6 not merge higher by 1')
a = A(range(30,101))

a.mergewithrange(range(102,150))

for rng in a.ranges:
    print(rng)

print('--7 not merge lower by 1')
a = A(range(30,101))

a.mergewithrange(range(5,29))

for rng in a.ranges:
    print(rng)