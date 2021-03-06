#! /usr/bin/python3
import sys, serial, time
import prometheus_client as prom

def Getfloat(lsb, msb):
  if msb > 127:
    value = -(float((msb ^ 255) + 1) * 256 - lsb) / 100
  else:
    value = float(msb * 256 + lsb) / 100
  return value

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
  try:
      ser.write(b'S?\r')
  except Exception as e:
      sys.exit("Seriele poort {} kan niet geschreven worden.\n{}: {}".format(ser.name, type(e).__name__, str(e)))

  try:
      ig_raw = ser.read(32)
  except Exception as e:
      sys.exit("Seriele poort {} kan niet gelezen worden.\n{}: {}".format(ser.name, type(e).__name__, str(e)))

  data = {};
  if len(ig_raw) == 32:
    data['timestamp']          = unixtime_utc
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
