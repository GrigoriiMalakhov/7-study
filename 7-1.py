import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
GPIO.setmode(GPIO.BCM)  

dac = [26, 19, 13, 6, 5, 11, 9, 10]
cad = [10, 9, 11, 5, 6, 13, 19, 26]
mas = [0, 0, 0, 0, 0, 0, 0, 0]
leds = [24, 25, 8, 7, 12, 16, 20, 21]
led = []

times_str = []
measure = []
measure_str = []   

i = 0
comp = 4
troyka = 17
beginning_time = time.time()
time_now = time.time() - beginning_time

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]
def adc():
   
    for i in 7, 6, 5, 4, 3, 2, 1, 0:
        GPIO.output(cad[i], 1)
        mas[7 - i] = 1
        time.sleep(0.007)
        if(GPIO.input(comp) == 0):
            GPIO.output(cad[i], 0)
            mas[7-i] = 0
              
try:
    while(1):
        GPIO.output(troyka, 1)
        v = 0
        mas = [0, 0, 0, 0, 0, 0, 0, 0]
        GPIO.output(dac, mas)
        adc()
       
        for j in range(8):
            v += mas[j]*(2**(7-j))
        volt = v*3.3/256
        print(v, "  ", volt)
        GPIO.output(leds, 0)
       
        k = 0
        for k in range(9):
            if(v < k * 32 + 5):
                j = 0
                for j in range(k):
                    GPIO.output(leds[j], 1)
                break  
        measure.append(volt)
        measure_str.append(str(volt))
        if volt >= 0.97*3.3:
            times_str.append(str(time_now))
            while volt >= 0.02*3.3:
                GPIO.output(troyka, 0)
                v = 0
                mas = [0, 0, 0, 0, 0, 0, 0, 0]
                GPIO.output(dac, mas)
                adc()
       
                for j in range(8):
                    v += mas[j]*(2**(7-j))
                volt = v*3.3/256
                print(v, "  ", volt)
                GPIO.output(leds, 0)
       
                k = 0
                for k in range(9):
                    if(v < k * 32 + 5):
                        j = 0
                        for j in range(k):
                            GPIO.output(leds[j], 1)
                        break  
                measure.append(volt)
                measure_str.append(str(volt))

finally:
    with open("data.txt", "w") as outfile:
            outfile.write("Новое измерение \n")
            outfile.write("\n".join(measure_str))
   
    t = time.time() - beginning_time
    print("Общее время измерений: ", t, "секунд")
    print("Период одного измерения: ", t / len(measure), "секунд")
    print("Средняя частота дискретизации измерений: ", (len(measure) / t), "герц")
    print("Шаг квантования АЦП: ", 3.3 * (t / len(measure)), "вольт")

    with open("settings.txt", "w") as outfile:
            outfile.write("Новое измерение")
            outfile.write("\nСредняя частота дискретизации измерений: ")
            outfile.write(str(len(measure) / t))
            outfile.write("\nШаг квантования АЦП: ")
            outfile.write(str(3.3 * t / len(measure)))
           
    GPIO.output(dac, 0)
    GPIO.cleanup()
    plt.plot(measure)
    plt.show()