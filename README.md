# Real-time-Safety-and-Hazard-Monitoring-System

The project focuses on real-time health and environmental safety monitoring using an ESP32 by integrating multiple biomedical and environmental sensors to continuously observe a user’s physical condition and surrounding air quality.

**Implementation:**
ESP32 collects data from sensors such as MPU6050 (fall detection), MAX30102 (heart rate & SpO₂), DHT11, MQ135, dust, and sound sensors, processes it in real time, and displays key parameters on an OLED while uploading data to the cloud (ThingSpeak).
Threshold-based logic triggers alerts through a buzzer/LED during abnormal or emergency conditions, ensuring timely awareness and safety.

