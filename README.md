Smart Attic is a system that leverages the potential of Internet-of-Things (IoT) technologies 
to address both the security and the safety issues that traditional attics pose. 
The system integrates a network of intelligent sensors to gather data about the attic environment 
and potential security breaches. This data is transmitted securely through secure 
communication protocols to a central hub (Raspberry Pi), where it is analyzed. Then, the system 
uses actuators that, based on the analysis done by the central hub, takes automated actions 
to ensure a swift and efficient response to security breaches or environmental threats.

# Run of web application

```
export DB_HOST = "your-database-host"
export DB_USERNAME = "your-db-username"
export DB_PASSWORD = "your-db-password"
export DB_NAME = "your-database-name"
cd webServer
python3 webServer.py
```
