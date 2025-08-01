from time import sleep
from components.heartbeat_led import HeartbeatLed
from components.gps_module import GPSModule
from utils.logger import setup_logger

heartbeat_led = HeartbeatLed(40)
gps = GPSModule(port='/dev/ttyS0', baudrate=9600)
logger = setup_logger("main")

try:
  gps.connect()
  
  while True:
    try:
      data = gps.read_position_informations()

      if data is None:
          continue

      has_fix = False

      if data["type"] == "GGA":
          has_fix = int(data.get("fix_quality", 0)) > 0
      elif data["type"] == "RMC":
          has_fix = data.get("status") == "A"

      if has_fix:
          heartbeat_led.turn_on()
      else:
          heartbeat_led.blink()

      logger.info(f"Localização: {data}")
      print(f"🔄 Nova leitura: {data}")

      sleep(1)

    except Exception as e:
      logger.info(f"Erro inesperado: {e}")

except KeyboardInterrupt:
  logger.info("Encerrando execução.")
  print('Bye! =)')

finally:
  gps.close()
  heartbeat_led.turn_off()


