# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
BUZZER_PIN = 25  # تعيين المنفذ المستخدم للبازر

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)  # تعيين المنفذ الخاص بالبازر كمخرج

def distance():
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    
    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    
    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    # Time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    return distance

def main():
    try:
        while True:
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            if dist < 30:  # إذا كانت المسافة أقل من 30 سم
                GPIO.output(BUZZER_PIN, GPIO.HIGH)  # تشغيل البازر
            else:
                GPIO.output(BUZZER_PIN, GPIO.LOW)  # إيقاف البازر
            time.sleep(1)
    
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

if __name__ == '__main__':
    main()  # استدعاء الدالة الرئيسية
