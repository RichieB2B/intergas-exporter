#! /usr/bin/python3
import sys, serial, time
import prometheus_client as prom

def Get_int(lsb, msb):
    value = int(msb * 256 + lsb)
    return value

def Get_int32(bytelist):
    value = bytelist[3] * 16777216 + bytelist[2] * 65536 + bytelist[1] * 256 + bytelist[0]
    return value

def Getfloat(lsb, msb):
  if msb > 127:
    value = -(float((msb ^ 255) + 1) * 256 - lsb) / 100
  else:
    value = float(msb * 256 + lsb) / 100
  return value

def Get_CRC(byte1, byte2, byte3, byte4):
    hexstr1 = hex(byte1)[2:]
    hexstr2 = hex(byte2)[2:]
    hexstr3 = hex(byte3)[2:]
    hexstr4 = hex(byte4)[2:]
    hexstr_list = [
     hexstr1, hexstr2, hexstr3, hexstr4]
    crc = ''
    for string in hexstr_list:
        if len(string) == 1:
            string = '0' + string
        crc = crc + string
    return crc

def read_raw(ser, command):
  try:
      ser.write(command)
  except Exception as e:
      sys.exit("Seriele poort {} kan niet geschreven worden.\n{}: {}".format(ser.name, type(e).__name__, str(e)))

  try:
      raw = ser.read(32)
  except Exception as e:
      sys.exit("Seriele poort {} kan niet gelezen worden.\n{}: {}".format(ser.name, type(e).__name__, str(e)))

  return raw

def read_status(ser):
  ig_raw = read_raw(ser, b'S?\r')
  data = {};
  if len(ig_raw) == 32:
    data['t_aanvoer']          = Getfloat(ig_raw[0] , ig_raw[1])
    data['t_flow']             = Getfloat(ig_raw[2] , ig_raw[3])
    data['t_retour']           = Getfloat(ig_raw[4] , ig_raw[5])
    data['t_warmw']            = Getfloat(ig_raw[6] , ig_raw[7])
    data['t_boiler']           = Getfloat(ig_raw[8] , ig_raw[9])
    data['t_buiten']           = Getfloat(ig_raw[10], ig_raw[11])
    data['ch_pressure']        = Getfloat(ig_raw[12], ig_raw[13])
    data['temp_set']           = Getfloat(ig_raw[14], ig_raw[15])
    data['fanspeed_set']       = Getfloat(ig_raw[16], ig_raw[17]) * 100
    data['fanspeed']           = Getfloat(ig_raw[18], ig_raw[19]) * 100
    data['fan_pwm']            = Getfloat(ig_raw[20], ig_raw[21]) * 10
    data['io_curr']            = Getfloat(ig_raw[22], ig_raw[23])
    data['displ_code']         = ig_raw[24]
    data['gp_switch']          = bool(ig_raw[26] &  1 << 7)
    data['tap_switch']         = bool(ig_raw[26] &  1 << 6)
    data['roomtherm']          = bool(ig_raw[26] &  1 << 5)
    data['pump']               = bool(ig_raw[26] &  1 << 4)
    data['dwk']                = bool(ig_raw[26] &  1 << 3)
    data['alarm_status']       = bool(ig_raw[26] &  1 << 2)
    data['ch_cascade_relay']   = bool(ig_raw[26] &  1 << 1)
    data['opentherm']          = bool(ig_raw[26] &  1 << 0)
    data['gasvalve']           = bool(ig_raw[28] &  1 << 7)
    data['spark']              = bool(ig_raw[28] &  1 << 6)
    data['io_signal']          = bool(ig_raw[28] &  1 << 5)
    data['ch_ot_disabled']     = bool(ig_raw[28] &  1 << 4)
    data['low_water_pressure'] = bool(ig_raw[28] &  1 << 3)
    data['pressure_sensor']    = bool(ig_raw[28] &  1 << 2)
    data['burner_block']       = bool(ig_raw[28] &  1 << 1)
    data['grad_flag']          = bool(ig_raw[28] &  1 << 0)

    # Change display code if a fault occurred
    if ig_raw[27] == 128:
      fault_code = ig_raw[29]
      data['displ_code'] = fault_code + 256

    # Known display codes (see also https://github.com/rickvanderzwet/IntergasBoilerReader/blob/trunk/intergas_prestige_cw6.py)
    # 0:   "CV brandt",
    # 51:  "Warm water",
    # 102: "CV brandt",
    # 126: "CV in rust",
    # 204: "Tapwater nadraaien",
    # 231: "CV nadraaien",

    return data

def read_crc(ser):
  ig_raw = read_raw(ser, b'CRC')

  data = {};
  if len(ig_raw) == 32:
      data['interrupt_time']    = Get_int(ig_raw[0], ig_raw[1]) / float(5)
      data['interrupt_load']    = Get_int(ig_raw[2], ig_raw[3]) / 6.25
      data['main_load']         = Get_int(ig_raw[4], ig_raw[5]) / float(8)
      freq_number               = Get_int(ig_raw[6], ig_raw[7])
      if freq_number > 0:
          data['net_frequency'] = float(2000) / freq_number
      else:
          data['net_frequency'] = 0
      data['voltage_reference'] = Get_int(ig_raw[8], ig_raw[9]) * 5 / float(1024)
      data['checksum1']         = Get_CRC(ig_raw[24], ig_raw[25], ig_raw[26], ig_raw[27])
      data['checksum2']         = Get_CRC(ig_raw[28], ig_raw[29], ig_raw[30], ig_raw[31])

  return data

def read_hours(ser):
  ig_raw = read_raw(ser, b'HN\r')

  data = {};
  if len(ig_raw) == 32:
      data['line_power_connected']  = Get_int(ig_raw[0], ig_raw[1]) + ig_raw[30] * 65536
      data['line_power_disconnect'] = Get_int(ig_raw[2], ig_raw[3])
      data['ch_function']           = Get_int(ig_raw[4], ig_raw[5])
      data['dhw_function']          = Get_int(ig_raw[6], ig_raw[7])
      data['burnerstarts']          = Get_int(ig_raw[8], ig_raw[9]) + ig_raw[31] * 65536
      data['ignition_failed']       = Get_int(ig_raw[10], ig_raw[11])
      data['flame_lost']            = Get_int(ig_raw[12], ig_raw[13])
      data['reset']                 = Get_int(ig_raw[14], ig_raw[15])
      data['gasmeter_cv']           = Get_int32(ig_raw[16:20]) / float(10000)
      data['gasmeter_dhw']          = Get_int32(ig_raw[20:24]) / float(10000)

  return data

def read_intergas():
  # Set COM port config
  ser = serial.Serial()
  ser.baudrate = 9600
  ser.timeout=10
  ser.port="/dev/ttyUSB0"

  # Open COM port
  try:
      ser.open()
  except Exception as e:
      sys.exit("Fout bij het openen van {}.\n{}: {}".format(ser.name, type(e).__name__, str(e)))

  unixtime_utc = time.time()

  data = {}
  data.update(read_status(ser))
  data.update(read_crc(ser))
  data.update(read_hours(ser))

  if data:
    data['timestamp']  = unixtime_utc

  # Close port and show status
  try:
      ser.close()
  except Exception as e:
      sys.exit("Fout blij sluiten van {}.\n{}: {}".format(ser.name, type(e).__name__, str(e)))

  return data

if __name__ == '__main__':
  temp        = prom.Gauge('intergas_temperature_celcius'           , 'Temperature in celsius', ['type'])
  pressure    = prom.Gauge('intergas_water_pressure_bar'            , 'Water pressure in bar')
  dispcode    = prom.Gauge('intergas_display_code'                  , 'Display code')
  f_speed     = prom.Gauge('intergas_fanspeed_rpm'                  , 'Fan speed in rpm', ['type'])
  f_pwm       = prom.Gauge('intergas_fan_pwm'                       , 'Fan PWM duty cycle percentage')
  flag        = prom.Gauge('intergas_flag'                          , 'Boolean flags', ['name'])
  io_curr     = prom.Gauge('intergas_ionization_current_microampere', 'Ionization current in µA')
  int_time    = prom.Gauge('intergas_interrupt_time'                , 'Interupt time')
  load        = prom.Gauge('intergas_load'                          , 'Load %', ['type'])
  hours       = prom.Gauge('intergas_hours'                         , 'Duration in hours', ['type'])
  stats       = prom.Gauge('intergas_stats'                         , 'Statistics in number of times', ['type'])
  gasmeter    = prom.Gauge('intergas_gasmeter'                      , 'Gas usage in m3', ['type'])
  updated     = prom.Gauge('intergas_updated'                       , 'Intergas client last updated')
  up          = prom.Gauge('intergas_up'                            , 'Intergas client status')
  prom.start_http_server(8080)

  while True:
    ig=read_intergas()
    if ig:
      up.set(1)
      updated.set(ig['timestamp'])
      temp.labels('aanvoer').set(ig['t_aanvoer'])
      temp.labels('flow').set(ig['t_flow'])
      temp.labels('retour').set(ig['t_retour'])
      temp.labels('warmwater').set(ig['t_warmw'])
      temp.labels('set').set(ig['temp_set'])
      pressure.set(ig['ch_pressure'])
      dispcode.set(ig['displ_code'])
      f_speed.labels('set').set(ig['fanspeed_set'])
      f_speed.labels('measured').set(ig['fanspeed'])
      f_pwm.set(ig['fan_pwm'])
      io_curr.set(ig['io_curr'])
      int_time.set(ig['interrupt_time'])
      load.labels('interrupt').set(ig['interrupt_load'])
      load.labels('main').set(ig['main_load'])
      hours.labels('line_power').set(ig['line_power_connected'])
      hours.labels('ch_function').set(ig['ch_function'])
      hours.labels('dhw_function').set(ig['dhw_function'])
      stats.labels('power_disconnect').set(ig['line_power_disconnect'])
      stats.labels('burnerstarts').set(ig['burnerstarts'])
      stats.labels('ignition_failed').set(ig['ignition_failed'])
      stats.labels('flame_lost').set(ig['flame_lost'])
      stats.labels('reset').set(ig['reset'])
      gasmeter.labels('cv').set(ig['gasmeter_cv'])
      gasmeter.labels('warmwater').set(ig['gasmeter_dhw'])

      flag.labels('gp_switch').set(ig['gp_switch'])
      flag.labels('tap_switch').set(ig['tap_switch'])
      flag.labels('roomtherm').set(ig['roomtherm'])
      flag.labels('pump').set(ig['pump'])
      flag.labels('dwk').set(ig['dwk'])
      flag.labels('alarm_status').set(ig['alarm_status'])
      flag.labels('ch_cascade_relay').set(ig['ch_cascade_relay'])
      flag.labels('opentherm').set(ig['opentherm'])
      flag.labels('gasvalve').set(ig['gasvalve'])
      flag.labels('spark').set(ig['spark'])
      flag.labels('io_signal').set(ig['io_signal'])
      flag.labels('ch_ot_disabled').set(ig['ch_ot_disabled'])
      flag.labels('low_water_pressure').set(ig['low_water_pressure'])
      flag.labels('pressure_sensor').set(ig['pressure_sensor'])
      flag.labels('burner_block').set(ig['burner_block'])
      flag.labels('grad_flag').set(ig['grad_flag'])
    else:
      up.set(0)

    time.sleep(5)
