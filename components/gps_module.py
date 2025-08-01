import serial
import pynmea2

from utils.logger import setup_logger

class GPSModule:
    def __init__(self, port='/dev/ttyS0', baudrate=9600, timeout=1):
        self.logger = setup_logger("gps")
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None

    def connect(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.logger.info(f"Conectado à porta serial: {self.port}")
        except serial.SerialException as e:
            self.logger.info(f"Erro ao conectar na porta serial: {e}")
            raise

    def read_sentence(self):
        if self.serial_conn is None:
            raise RuntimeError("A conexão serial não foi iniciada. Chame 'connect()' antes.")

        try:
            line = self.serial_conn.readline().decode('ascii', errors='ignore').strip()

            if not line.startswith('$'):
                return None

            try:
                msg = pynmea2.parse(line)
                return msg
            except pynmea2.ParseError as e:
                self.logger.warning(f"Erro ao interpretar NMEA: {e}")
                return None

        except pynmea2.ParseError:
            return None
        except UnicodeDecodeError:
            return None
        except Exception as e:
            self.logger.error(f"Erro inesperado ao ler do GPS: {e}")
            return None

    def read_position_informations(self):
        msg = self.read_sentence()

        if msg is None:
            return None

        if isinstance(msg, pynmea2.GGA):
            return {
                "type": "GGA",
                "latitude": msg.latitude,
                "longitude": msg.longitude,
                "altitude": msg.altitude,
                "num_sats": msg.num_sats,
                "timestamp": msg.timestamp,
                "fix_quality": msg.gps_qual
            }

        elif isinstance(msg, pynmea2.RMC):
            return {
                "type": "RMC",
                "latitude": msg.latitude,
                "longitude": msg.longitude,
                "speed": msg.spd_over_grnd,
                "true_course": msg.true_course,
                "datestamp": msg.datestamp,
                "timestamp": msg.timestamp,
                "status": msg.status
            }

        return None

    def close(self):
        if self.serial_conn:
            self.serial_conn.close()
            self.logger.info("Conexão serial encerrada.")
