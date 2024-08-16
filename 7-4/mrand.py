from mrand_seed import drng

class MRGRand:
    __NORM    = 2.328306549295728e-10  
    __NORM2   = 2.328318825240738e-10  
    __M1      = 4294967087.0
    __M2      = 4294944443.0
    
    def GetRand(self, stream):
        global drng  # Ensure we are using the global variable

        s10 = drng[stream][0]
        s11 = drng[stream][1]
        s12 = drng[stream][2]
        s20 = drng[stream][3]
        s21 = drng[stream][4]
        s22 = drng[stream][5]

        p = 1403580.0 * s11 - 810728.0 * s10
        k = p // self.__M1
        p -= k * self.__M1
        if p < 0.0:
            p += self.__M1
        s10 = s11
        s11 = s12
        s12 = p

        p = 527612.0 * s22 - 1370589.0 * s20
        k = p // self.__M2
        p -= k * self.__M2
        if p < 0.0:
            p += self.__M2
        s20 = s21
        s21 = s22
        s22 = p

        drng[stream][0] = s10
        drng[stream][1] = s11
        drng[stream][2] = s12
        drng[stream][3] = s20
        drng[stream][4] = s21
        drng[stream][5] = s22

        if s12 <= s22:
            return (s12 - s22 + self.__M1) * self.__NORM
        else:
            return (s12 - s22) * self.__NORM
    
    # Set seed vector for stream "stream"
    # seed is and Array(6) and stream is an integer
    def SetSeed(self, seed, stream):
        for x in range(6):
            drng[stream][x] = seed[x]
        

    # Get seed vector for stream "stream"
    # seed is and Array(6) and stream is an integer
    def GetSeed(self, seed, stream):
        for x in range(6):
            seed[x] = drng[stream][x]
