import spidev # type: ignore
import time

from utils.logger import setup_logger

# Endereços de comandos SPI do MCP2515
SPI_RESET = 0xC0
SPI_READ = 0x03
SPI_WRITE = 0x02
SPI_RTS = 0x80
SPI_READ_STATUS = 0xA0
SPI_BIT_MODIFY = 0x05

# Registradores MCP2515
CANSTAT = 0x0E
CANCTRL = 0x0F
TXB0CTRL = 0x30
RXB0CTRL = 0x60
CNF1 = 0x2A
CNF2 = 0x29
CNF3 = 0x28

# Modos de operação
MODE_NORMAL = 0x00
MODE_LOOPBACK = 0x40
MODE_CONFIG = 0x80

class MCP2515:
    def __init__(self, bus=0, device=0, speed=1000000):
        self.logger = setup_logger("can_module")
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = speed
        self.spi.mode = 0
        self.logger.info(f"SPI inicializado (bus={bus}, device={device}, speed={speed}Hz)")

    def _write_register(self, address, value):
        self.spi.xfer2([SPI_WRITE, address, value])
        self.logger.debug(f"Write 0x{value:02X} → reg 0x{address:02X}")

    def _read_register(self, address):
        val = self.spi.xfer2([SPI_READ, address, 0x00])[2]
        self.logger.debug(f"Read reg 0x{address:02X} = 0x{val:02X}")
        return val

    def _bit_modify(self, address, mask, value):
        self.spi.xfer2([SPI_BIT_MODIFY, address, mask, value])
        self.logger.debug(f"Bit modify reg 0x{address:02X}: mask=0x{mask:02X}, val=0x{value:02X}")

    def reset(self):
        self.spi.xfer2([SPI_RESET])
        self.logger.info("MCP2515 resetado")
        time.sleep(0.1)

    def read_status(self):
        status = self.spi.xfer2([SPI_READ_STATUS, 0x00])[1]
        self.logger.info(f"Status SPI: 0x{status:02X}")
        return status

    def set_mode(self, mode):
        self._bit_modify(CANCTRL, 0xE0, mode)
        time.sleep(0.05)
        actual_mode = self._read_register(CANSTAT) & 0xE0
        if actual_mode == mode:
            self.logger.info(f"✅ MCP2515 agora em modo {hex(mode)}")
            return True
        else:
            self.logger.error(f"❌ Falha ao entrar no modo {hex(mode)}, leu {hex(actual_mode)}")
            return False

    def init_loopback(self):
        """Inicializa o MCP2515 em modo loopback"""
        self.reset()
        # Entrar em modo configuração
        if not self.set_mode(MODE_CONFIG):
            return False

        # Configuração básica de temporização (para 125kbps, clock 8MHz)
        self._write_register(CNF1, 0x03)
        self._write_register(CNF2, 0x90)
        self._write_register(CNF3, 0x02)

        # Habilita recebimento de qualquer mensagem
        self._write_register(RXB0CTRL, 0x60)

        # Entra em modo loopback
        return self.set_mode(MODE_LOOPBACK)

    def test_loopback(self):
        """Envia e tenta receber mensagem no modo loopback"""
        self.logger.info("🧪 Testando modo loopback...")
        self._write_register(TXB0CTRL + 1, 0xAA)  # apenas dado simbólico
        self.spi.xfer2([SPI_RTS | 0x01])  # requisita transmissão
        time.sleep(0.1)
        received = self._read_register(RXB0CTRL + 1)
        self.logger.info(f"Mensagem recebida (loopback): 0x{received:02X}")

    def close(self):
        self.spi.close()
        self.logger.info("SPI fechado")


if __name__ == "__main__":
    mcp = MCP2515()
    try:
        if mcp.init_loopback():
            mcp.test_loopback()
        else:
            mcp.logger.error("Falha ao inicializar MCP2515 no modo loopback.")
    finally:
        mcp.close()